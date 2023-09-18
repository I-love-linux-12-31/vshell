import tarfile
import zipfile

from .vfs_classes import *
from .vfs_loaders import build_root_from_tar_info, build_root_from_zip_info


vfs_root = None
current_dir = "/"
vfs_current_dir_obj = None

mode_on_init = ""
archive_path_on_init = ""


def init(path: str, mode="auto"):
    global vfs_root
    global vfs_current_dir_obj

    global mode_on_init, archive_path_on_init

    if mode == "auto":
        if ".zip" in path:
            mode = "zip"
        elif ".tar" in path:
            mode = "tar"
        else:
            raise IOError("Not supported archive format! Use only .zip or .tar")

    archive_path_on_init = path
    mode_on_init = mode
    if mode == "zip":
        with zipfile.ZipFile(path, 'r') as zip_archive:
            vfs_root = build_root_from_zip_info(zip_archive.infolist())
    elif mode == "tar":
        with tarfile.TarFile.open(path) as tar:
            vfs_root = build_root_from_tar_info(tar.getmembers())
    else:
        raise IOError("Not supported mode! Use only 'zip' or 'tar' or 'auto' modes!")

    vfs_current_dir_obj = vfs_root


def simplify_path(path: str) -> str:
    stack = []
    for s in path.split('/'):
        if s in ('', '.'):
            continue
        if s == '..' and False:
            if stack:
                stack.pop()
        else:
            stack.append(s)

    if path.startswith('/'):
        return '/' + '/'.join(stack)
    return "./" + '/'.join(stack)


def get_object_by_path(path: str) -> VFSFile or VFSDirectory or VFSRoot:
    path = simplify_path(path)
    # if path == "..":
    #     return '/' + "/".join(vfs_current_dir_obj.path.split("/")[:-1])

    # print("\033[35mDBG:\033[0m Get object by path : ", path)
    if path == '/':
        # print("\033[35mDBG:\033[0m Get object by path : returned /")
        return vfs_root
    if path == './':
        # print("\033[35mDBG:\033[0m Get object by path : returned ./")
        return vfs_current_dir_obj

    if path.startswith("./"):
        path = current_dir + '/' + path[2:]
    if path.startswith("/"):
        cur = vfs_root
    else:
        cur = vfs_current_dir_obj

    # print(path)
    stack = simplify_path(path).split("/")
    # print(stack)
    if len(stack) > 1:
        stack = stack[1:]
    # print(path)
    # print(stack)
    path_before = []
    while stack:

        cur: VFSObject
        s = stack.pop(0)
        path_before.append(s)
        # print(f"\033[35mDBG:\033[0m path before {path_before} : now {s}")
        if s != ".." and s != "./..":
            cur = cur.find_item_by_name(s)
        else:
            req = '/'.join(path_before[:-2])
            # print("REQ: ", req)
            if req:
                cur = get_object_by_path(req)
            else:
                return vfs_root
    # print(f"\033[35mDBG: Get object by path : returned {cur}\033[0m")
    return cur


def is_path_exists(path: str) -> bool:
    try:
        obj = get_object_by_path(path)
    except Exception:
        return False
