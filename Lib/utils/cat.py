import tarfile
import zipfile

import Lib.vfs


def app(target):
    mode = Lib.vfs.mode_on_init
    path = Lib.vfs.archive_path_on_init
    if mode == "auto":
        if ".zip" in path:
            mode = "zip"
        elif ".tar" in path:
            mode = "tar"
        else:
            raise IOError("Not supported archive format! Use only .zip or .tar")

    archive_path_on_init = path
    if mode == "zip":
        with zipfile.ZipFile(archive_path_on_init, 'r') as zip_archive:
            with zip_archive.open(target) as f:
                for line in f:
                    print(line)
    elif mode == "tar":
        target = '.' + target
        with tarfile.TarFile.open(archive_path_on_init) as tar:
            f = tar.extractfile(target)
            content = f.read()
            print(content.decode("utf-8"))


def cat(*args, **kwargs):
    path = kwargs.setdefault("path", './')
    if len(args) > 0 and not args[0].startswith("-"):
        path = args[0]

    # print(path, "###")
    obj = Lib.vfs.get_object_by_path(path)
    if obj is None:
        print(f"\033[31mInvalid path!\033[0m")
        return
    if obj.__class__.__name__ != "VFSFile":
        print(f"\033[31mIs not a file!\033[0m")
        return
    path = obj.path
    if path.startswith("./"):
        path = Lib.vfs.simplify_path(Lib.vfs.vfs_current_dir_obj.path + "/" + path[2:])

    if not path.startswith('/'):
        path = '/' + path
    # print(f"\033[31mCAT: {path}\033[0m")
    app(path)
