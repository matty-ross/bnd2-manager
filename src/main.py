import tkinter, tkinter.filedialog

import bnd2

from manager import Manager


def unpack_bundle(bundle: bnd2.BundleV2, directory: str) -> None:
    manager = Manager(bundle, directory)
    bundle.load()
    manager.unpack()


def pack_bundle(bundle: bnd2.BundleV2, directory: str) -> None:
    manager = Manager(bundle, directory)
    manager.pack()
    bundle.save()


def main() -> None:
    tkinter.Tk().withdraw()

    file_names = tkinter.filedialog.askopenfilenames()
    bundles: list[bnd2.BundleV2] = []
    for file_name in file_names:
        bundle = bnd2.BundleV2(file_name)
        bundles.append(bundle)

    directory = tkinter.filedialog.askdirectory()

    action = input("[u]npack or [p]ack ? ")

    if action == 'u':
        for bundle in bundles:
            print(f"Unpacking bundle '{bundle.file_name}'...")
            unpack_bundle(bundle, directory)
            print("Done.")
    elif action == 'p':
        for bundle in bundles:
            print(f"Packing bundle '{bundle.file_name}'...")
            pack_bundle(bundle, directory)
            print("Done.")


if __name__ == '__main__':
    main()
