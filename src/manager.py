import pathlib

import bnd2

import bundle_file


class Manager:

    def __init__(self, bundle: bnd2.BundleV2, directory: str):
        self.bundle = bundle
        self.directory = pathlib.Path(directory)
        self.bundle_file = bundle_file.BundleFile(self.bundle_file_name)


    @property
    def bundle_name(self) -> str:
        return pathlib.Path(self.bundle.file_name).stem


    @property
    def bundle_file_name(self) -> str:
        file_name = (self.directory / (self.bundle_name + '_bundle')).with_suffix('.json')
        return str(file_name)


    @property
    def debug_data_file_name(self) -> str:
        file_name = (self.directory / (self.bundle_name + '_debug_data')).with_suffix('.xml')
        return str(file_name)


    def unpack(self) -> None:
        self.bundle_file.bundle.platform = self.bundle.platform.platform_type
        self.bundle_file.bundle.use_debug_data = bool(self.bundle.debug_data)
        self.bundle_file.bundle.use_zlib_compression = self.bundle.compressed
        self.bundle_file.bundle.resource_entries = []

        if self.bundle.debug_data:
            self._unpack_debug_data()
        
        for resource_entry in self.bundle.resource_entries:
            bundle_file_resource_entry = self._unpack_resource_entry(resource_entry)
            self.bundle_file.bundle.resource_entries.append(bundle_file_resource_entry)
            
        self.bundle_file.save()


    def pack(self) -> None:
        self.bundle_file.load()

        self.bundle.platform.platform_type = self.bundle_file.bundle.platform
        self.bundle.compressed = self.bundle_file.bundle.use_zlib_compression
        self.bundle.resource_entries = []

        for bundle_file_resource_entry in self.bundle_file.bundle.resource_entries:
            resource_entry = self._pack_resource_entry(bundle_file_resource_entry)
            self.bundle.resource_entries.append(resource_entry)

        if self.bundle_file.bundle.use_debug_data:
            self._pack_debug_data()


    def _unpack_debug_data(self) -> None:
        with open(self.debug_data_file_name, 'wb') as fp:
            fp.write(self.bundle.debug_data)


    def _unpack_resource_entry(self, resource_entry: bnd2.ResourceEntry) -> bundle_file.ResourceEntry:
        directory = self.directory / f'{resource_entry.type :08X}'
        if not directory.exists():
            directory.mkdir()

        for i in range(3):
            data = resource_entry.data[i]
            if data:
                file_name = (directory / f'{resource_entry.id :08X}_{i + 1}').with_suffix('.bin')
                with open(file_name, 'wb') as fp:
                    fp.write(data)

        bundle_file_resource_entry = bundle_file.ResourceEntry()
        bundle_file_resource_entry.id = resource_entry.id
        bundle_file_resource_entry.type = resource_entry.type
        bundle_file_resource_entry.import_entries = []
        
        for import_entry in resource_entry.import_entries:
            bundle_file_import_entry = bundle_file.ImportEntry()
            bundle_file_import_entry.id = import_entry.id
            bundle_file_import_entry.offset = import_entry.offset
            bundle_file_resource_entry.import_entries.append(bundle_file_import_entry)

        return bundle_file_resource_entry


    def _pack_debug_data(self) -> None:
        with open(self.debug_data_file_name, 'rb') as fp:
            self.bundle.debug_data = fp.read()


    def _pack_resource_entry(self, bundle_file_resource_entry: bundle_file.ResourceEntry) -> bnd2.ResourceEntry:
        resource_entry = bnd2.ResourceEntry()
        resource_entry.id = bundle_file_resource_entry.id
        resource_entry.type = bundle_file_resource_entry.type
        resource_entry.data = [b'', b'', b'']
        resource_entry.import_entries = []

        for bundle_file_import_entry in bundle_file_resource_entry.import_entries:
            import_entry = bnd2.ImportEntry()
            import_entry.id = bundle_file_import_entry.id
            import_entry.offset = bundle_file_import_entry.offset
            resource_entry.import_entries.append(import_entry)

        directory = self.directory / f'{resource_entry.type :08X}'

        for i in range(3):
            file_name = (directory / f'{resource_entry.id :08X}_{i + 1}').with_suffix('.bin')
            if file_name.exists():
                with open(file_name, 'rb') as fp:
                    resource_entry.data[i] = fp.read()

        return resource_entry
