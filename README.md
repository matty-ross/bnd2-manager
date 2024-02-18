# Burnout Paradise BundleV2 manager

![](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

A tool for unpacking and packing Burnout Paradise's BundleV2 files.


## Usage
```
cd .\src\
python .\main.py
```
### Unpacking
You will be prompted to choose bundles which you want to unpack.
Then you will choose a directory where to unpack their resources.
It will create directories with the resources and `xxx_bundle.json` files.
### Packing
You will be prompted to choose bundles which you want to pack.
Then you will choose a directory where the resources to pack are located.
It will pack the resources into the bundles based on the `xxx_bundle.json` files.

## About the xxx_bundle.json file
It represents the bnd2 file in a human readable, easy to edit format.
The `xxx` part is replaced with the bundle's name.
```json
{
    "platform": "PC",
    "use_debug_data": true,
    "use_zlib_compression": true,
    "resource_entries": [
        {
            "id": "DEADBEEF",
            "type": "0000000C",
            "import_entries": [
                {
                    "id": "FACEFEED",
                    "offset": "00000020"
                },
                {
                    "id": "C0FFEE77",
                    "offset": "00000040"
                }
            ]
        }
    ]
}
```
