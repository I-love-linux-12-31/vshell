import Lib.vfs


def cd(path: str = './', *args, **kwargs):
    new_path = Lib.vfs.simplify_path(path)
    try:
        if new_path.startswith('/'):
            Lib.vfs.current_dir = new_path
            Lib.vfs.vfs_current_dir_obj = Lib.vfs.get_object_by_path(new_path)
        else:
            # if Lib.vfs.vfs_current_dir_obj.path == "/":
            #     if path.startswith("./"):
            #         path = '/' + path[2:]

            candidate = Lib.vfs.get_object_by_path(path)
            if candidate.__class__.__name__ in ("VFSDirectory", "VFSRoot"):
                Lib.vfs.vfs_current_dir_obj = candidate
                Lib.vfs.current_dir = Lib.vfs.vfs_current_dir_obj.path
            else:
                print("\033[31mError!\033[0mIt is not a directory!")
    except Exception as e:
        print("\033[31mError!\033[0m path is invalid!")
