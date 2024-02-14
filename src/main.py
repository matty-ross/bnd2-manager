import tkinter, tkinter.filedialog

import bnd2

from manager import Manager


def unpack_bundle() -> None:
    file_name = tkinter.filedialog.askopenfilename()    
    bundle = bnd2.BundleV2(file_name)
    bundle.load()
    
    directory = tkinter.filedialog.askdirectory()
    manager = Manager(bundle, directory)
    manager.unpack()


def pack_bundle() -> None:
    pass


def main() -> None:
    tkinter.Tk().withdraw()

    action = input("[u]npack or [p]ack ? ")

    if action == 'u':
        unpack_bundle()
    elif action == 'p':
        pack_bundle()    


if __name__ == '__main__':
    main()
