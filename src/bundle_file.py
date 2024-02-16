import json
from dataclasses import dataclass

import bnd2


BND2_PLATFORM_FROM_STRING = {
    'PC': bnd2.PlatformType.PC,
    'XBOX_360': bnd2.PlatformType.XBOX_360,
    'PS3': bnd2.PlatformType.PS3,
}

BND2_PLATFORM_TO_STRING = {
    bnd2.PlatformType.PC: 'PC',
    bnd2.PlatformType.XBOX_360: 'XBOX_360',
    bnd2.PlatformType.PS3: 'PS3',
}


@dataclass
class ResourceEntry:
    id: int = None
    type: int = None
    imports_offset: int = None
    imports_count: int = None


@dataclass
class Bundle:
    platform: bnd2.PlatformType = None
    use_debug_data: bool = None
    use_zlib_compression: bool = None
    resource_entries: list[ResourceEntry] = None


class BundleFile:
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.bundle = Bundle()


    def load(self) -> None:
        with open(self.file_name, 'r') as fp:
            json_bundle = json.load(fp)
        
        self.bundle.platform = BND2_PLATFORM_FROM_STRING[json_bundle['platform']]
        self.bundle.use_debug_data = json_bundle['use_debug_data']
        self.bundle.use_zlib_compression = json_bundle['use_zlib_compression']
        self.bundle.resource_entries = []

        for json_resource_entry in json_bundle['resource_entries']:
            resource_entry = ResourceEntry()
            resource_entry.id = int(json_resource_entry['id'], 16)
            resource_entry.type = int(json_resource_entry['type'], 16)
            resource_entry.imports_offset = int(json_resource_entry['imports_offset'], 16) if not json_resource_entry['imports_offset'] is None else None
            resource_entry.imports_count = json_resource_entry['imports_count']
            self.bundle.resource_entries.append(resource_entry)


    def save(self) -> None:
        json_bundle = {}
        json_bundle['platform'] = BND2_PLATFORM_TO_STRING[self.bundle.platform]
        json_bundle['use_debug_data'] = self.bundle.use_debug_data
        json_bundle['use_zlib_compression'] = self.bundle.use_zlib_compression
        json_bundle['resource_entries'] = []

        for resource_entry in self.bundle.resource_entries:
            json_resource_entry = {}
            json_resource_entry['id'] = f'{resource_entry.id :08X}'
            json_resource_entry['type'] = f'{resource_entry.type :08X}'
            json_resource_entry['imports_offset'] = f'{resource_entry.imports_offset :08X}' if not resource_entry.imports_offset is None else None
            json_resource_entry['imports_count'] = resource_entry.imports_count
            json_bundle['resource_entries'].append(json_resource_entry)

        with open(self.file_name, 'w') as fp:
            json.dump(json_bundle, fp, indent=4)
