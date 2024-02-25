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
class ImportEntry:
    id: int = None
    offset: int = None


@dataclass
class ResourceEntry:
    id: int = None
    type: int = None
    import_entries: list[ImportEntry] = None


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
            resource_entry.import_entries = []

            for json_import_entry in json_resource_entry['import_entries']:
                import_entry = ImportEntry()
                import_entry.id = int(json_import_entry['id'], 16)
                import_entry.offset = int(json_import_entry['offset'], 16)
                resource_entry.import_entries.append(import_entry)

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
            json_resource_entry['import_entries'] = []

            for import_entry in resource_entry.import_entries:
                json_import_entry = {}
                json_import_entry['id'] = f'{import_entry.id :08X}'
                json_import_entry['offset'] = f'{import_entry.offset :08X}'
                json_resource_entry['import_entries'].append(json_import_entry)

            json_bundle['resource_entries'].append(json_resource_entry)

        with open(self.file_name, 'w') as fp:
            json.dump(json_bundle, fp, indent=4)
