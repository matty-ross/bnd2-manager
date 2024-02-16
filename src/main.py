import tkinter, tkinter.filedialog

import bnd2

from manager import Manager


def unpack_bundle() -> None:
    file_name = tkinter.filedialog.askopenfilename()    
    directory = tkinter.filedialog.askdirectory()
    
    bundle = bnd2.BundleV2(file_name)
    manager = Manager(bundle, directory)
    bundle.load()
    manager.unpack()


def pack_bundle() -> None:
    file_name = tkinter.filedialog.askopenfilename()
    directory = tkinter.filedialog.askdirectory()
    
    bundle = bnd2.BundleV2(file_name)
    manager = Manager(bundle, directory)
    manager.pack()
    bundle.save()


def main() -> None:
    tkinter.Tk().withdraw()

    action = input("[u]npack or [p]ack ? ")

    if action == 'u':
        unpack_bundle()
    elif action == 'p':
        pack_bundle()    


if __name__ == '__main__':
    main()
