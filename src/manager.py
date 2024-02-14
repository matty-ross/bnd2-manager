import pathlib

import bnd2


class Manager:

    def __init__(self, bundle: bnd2.BundleV2, directory: str):
        self.bundle = bundle
        self.directory = pathlib.Path(directory)


    def unpack(self) -> None:
        self._unpack_debug_data()
        for resource_entry in self.bundle.resource_entries:
            self._unpack_resource_data(resource_entry)


    def pack(self) -> None:
        pass


    def _unpack_debug_data(self) -> None:
        debug_data = self.bundle.debug_data
        if debug_data:
            file_name = self.directory / 'debug_data.xml'
            with open(file_name, 'wb') as fp:
                fp.write(debug_data)


    def _unpack_resource_data(self, resource_entry: bnd2.ResourceEntry) -> None:
        directory = self.directory / f'{resource_entry.type :08X}'
        if not directory.exists():
            directory.mkdir()

        for i in range(3):
            data = resource_entry.data[i]
            if data:
                file_name = directory / f'{resource_entry.id :08X}_{i + 1}.bin'
                with open(file_name, 'wb') as fp:
                    fp.write(data)
