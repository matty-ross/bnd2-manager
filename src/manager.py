import pathlib
import json
from dataclasses import dataclass

import bnd2


RESOURCE_ENTRIES_FILE_NAME = 'resource_entries.json'
DEBUG_DATA_FILE_NAME = 'debug_data.xml'


@dataclass
class Entry:
    id: int = None
    type: int = None
    imports_offset: int = None
    imports_count: int = None

    def to_dict(self) -> dict:
        entry = {
            'id': f'{self.id :08X}',
            'type': f'{self.type :08X}',
            'imports_offset': f'{self.imports_offset :08X}' if self.imports_count > 0 else None,
            'imports_count': self.imports_count if self.imports_count > 0 else None,
        }
        return entry
    
    def from_dict(self, entry: dict) -> None:
        self.id = int(entry['id'], 16)
        self.type = int(entry['type'], 16)
        self.imports_offset = int(entry['imports_offset'], 16)
        self.imports_count = int(entry['imports_count'])


class Manager:

    def __init__(self, bundle: bnd2.BundleV2, directory: str):
        self.bundle = bundle
        self.directory = pathlib.Path(directory)


    def unpack(self) -> None:
        if self.bundle.debug_data:
            self._unpack_debug_data()
        
        entries = []
        for resource_entry in self.bundle.resource_entries:
            entry = self._unpack_resource_entry(resource_entry)
            entries.append(entry.to_dict())

        with open(self.directory / RESOURCE_ENTRIES_FILE_NAME, 'w') as fp:
            json.dump(entries, fp, indent=4)


    def pack(self, use_debug_data: bool, use_zlib_compression: bool) -> None:
        with open(self.directory / RESOURCE_ENTRIES_FILE_NAME, 'r') as fp:
            entries = json.load(fp)

        self.bundle.resource_entries.clear()
        for entry in entries:
            resource_entry = self._pack_resource_data(Entry().from_dict(entry))
            self.bundle.resource_entries.append(resource_entry)

        if use_debug_data:
            self._pack_debug_data()
        
        self.bundle.compressed = use_zlib_compression


    def _unpack_debug_data(self) -> None:
        file_name = self.directory / DEBUG_DATA_FILE_NAME
        with open(file_name, 'wb') as fp:
            fp.write(self.bundle.debug_data)


    def _unpack_resource_entry(self, resource_entry: bnd2.ResourceEntry) -> Entry:
        directory = self.directory / f'{resource_entry.type :08X}'
        if not directory.exists():
            directory.mkdir()

        imports_count = len(resource_entry.import_entries)
        imports_offset = len(resource_entry.data[0])

        self.bundle.store_import_entries(resource_entry, imports_offset)

        for i in range(3):
            data = resource_entry.data[i]
            if data:
                file_name = directory / f'{resource_entry.id :08X}_{i + 1}.bin'
                with open(file_name, 'wb') as fp:
                    fp.write(data)

        entry = Entry()
        entry.id = resource_entry.id
        entry.type = resource_entry.type
        entry.imports_offset = imports_offset if imports_count > 0 else None
        entry.imports_count = imports_count if imports_count > 0 else None
        
        return entry


    def _pack_debug_data(self) -> None:
        file_name = self.directory / DEBUG_DATA_FILE_NAME
        with open(file_name, 'rb') as fp:
            self.bundle.debug_data = fp.read()


    def _pack_resource_data(self, entry: Entry) -> bnd2.ResourceEntry:
        resource_entry = bnd2.ResourceEntry()
        resource_entry.id = entry.id
        resource_entry.type = entry.type
        resource_entry.data = []

        directory = self.directory / f'{resource_entry.type :08X}'

        for i in range(3):
            file_name = directory / f'{resource_entry.id :08X}_{i + 1}.bin'
            data = b''
            if file_name.exists():
                with open(file_name, 'rb') as fp:
                    data = fp.read()
            resource_entry.data.append(data)

        self.bundle.load_import_entries(resource_entry, entry.imports_count, entry.imports_offset)

        return resource_entry
