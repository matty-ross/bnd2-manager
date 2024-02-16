import pathlib

import bnd2

import bundle_file


BUNDLE_FILE_NAME = 'bundle.json'
DEBUG_DATA_FILE_NAME = 'debug_data.xml'


class Manager:

    def __init__(self, bundle: bnd2.BundleV2, directory: str):
        self.bundle = bundle
        self.directory = pathlib.Path(directory)
        self.bundle_file = bundle_file.BundleFile(self.directory / BUNDLE_FILE_NAME)


    def unpack(self) -> None:
        self.bundle_file.bundle.platform = self.bundle.platform.platform_type
        self.bundle_file.bundle.use_debug_data = bool(self.bundle.debug_data)
        self.bundle_file.bundle.use_zlib_compression = self.bundle.compressed
        self.bundle_file.bundle.resource_entries = []

        if self.bundle.debug_data:
            self._unpack_debug_data()
        
        for resource_entry in self.bundle.resource_entries:
            entry = self._unpack_resource_entry(resource_entry)
            self.bundle_file.bundle.resource_entries.append(entry)
            
        self.bundle_file.save()


    def pack(self) -> None:
        self.bundle_file.load()

        self.bundle.resource_entries.clear()
        for entry in self.bundle_file.bundle.resource_entries:
            resource_entry = self._pack_resource_entry(entry)
            self.bundle.resource_entries.append(resource_entry)

        if self.bundle_file.bundle.use_debug_data:
            self._pack_debug_data()
        
        self.bundle.platform.platform_type = self.bundle_file.bundle.platform
        self.bundle.compressed = self.bundle_file.bundle.use_zlib_compression


    def _unpack_debug_data(self) -> None:
        file_name = self.directory / DEBUG_DATA_FILE_NAME
        with open(file_name, 'wb') as fp:
            fp.write(self.bundle.debug_data)


    def _unpack_resource_entry(self, resource_entry: bnd2.ResourceEntry) -> bundle_file.ResourceEntry:
        directory = self.directory / f'{resource_entry.type :08X}'
        if not directory.exists():
            directory.mkdir()

        imports_offset = len(resource_entry.data[0])
        imports_count = len(resource_entry.import_entries)

        self.bundle.store_import_entries(resource_entry, imports_offset)

        for i in range(3):
            data = resource_entry.data[i]
            if data:
                file_name = directory / f'{resource_entry.id :08X}_{i + 1}.bin'
                with open(file_name, 'wb') as fp:
                    fp.write(data)

        entry = bundle_file.ResourceEntry()
        entry.id = resource_entry.id
        entry.type = resource_entry.type
        entry.imports_offset = imports_offset if imports_count > 0 else None
        entry.imports_count = imports_count if imports_count > 0 else None

        return entry


    def _pack_debug_data(self) -> None:
        file_name = self.directory / DEBUG_DATA_FILE_NAME
        with open(file_name, 'rb') as fp:
            self.bundle.debug_data = fp.read()


    def _pack_resource_entry(self, entry: bundle_file.ResourceEntry) -> bnd2.ResourceEntry:
        resource_entry = bnd2.ResourceEntry()
        resource_entry.id = entry.id
        resource_entry.type = entry.type
        resource_entry.data = [b'', b'', b'']

        directory = self.directory / f'{resource_entry.type :08X}'

        for i in range(3):
            file_name = directory / f'{resource_entry.id :08X}_{i + 1}.bin'
            if file_name.exists():
                with open(file_name, 'rb') as fp:
                    resource_entry.data[i] = fp.read()

        self.bundle.load_import_entries(resource_entry, entry.imports_count, entry.imports_offset)

        return resource_entry
