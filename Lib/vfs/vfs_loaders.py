import stat
import tarfile
import zipfile
import Lib.vfs.vfs_classes as vfs_classes


def get_access_string_from_tar_info(info: tarfile.TarInfo) -> str:
    if info.isdir():
        res = "d"
    else:
        res = "-"
    flags = oct(info.mode)[2:]
    # res: DRWXRWXRWX
    for i in flags:
        # i: RWX
        match i:
            case '0':
                res += "---"
            case '1':
                res += "--x"
            case '2':
                res += "-w-"
            case '3':
                res += "-wx"
            case '4':
                res += "r--"
            case '5':
                res += "r-x"
            case '6':
                res += "rw-"
            case '7':
                res += "rwx"

    return res


def build_root_from_zip_info(infolist: [...]):
    root = vfs_classes.VFSRoot()
    for node in infolist:
        # print(node)
        node: zipfile.ZipInfo
        path = node.filename.strip("./").strip("/").split("/")
        name = path[-1]
        current_dir = root

        for item in path[:-1]:
            current_dir = current_dir.find_item_by_name(item)

        access_flags = node.external_attr >> 16
        if access_flags:
            access = stat.filemode(access_flags)
        else:
            access = None

        if node.is_dir():
            obj = vfs_classes.VFSDirectory(name=name, date=node.date_time, access=access)
        else:
            obj = vfs_classes.VFSFile(name=name, date=node.date_time, access=access, size=node.file_size)

        current_dir.items.append(obj)

    return root


def build_root_from_tar_info(infolist: [...]):
    root = vfs_classes.VFSRoot()
    passed_paths = set()
    for node in infolist:
        node: tarfile.TarInfo
        if node.name in passed_paths:
            continue
        else:
            passed_paths.add(node.name)
        # print(node)
        path = node.name.strip("./").strip("/").split("/")
        name = path[-1]
        current_dir = root

        for item in path[:-1]:
            current_dir = current_dir.find_item_by_name(item)

        access_flags = get_access_string_from_tar_info(node)

        if node.isdir():
            obj = vfs_classes.VFSDirectory(name=name, date=node.mtime, access=access_flags, path=node.path)
        else:
            obj = vfs_classes.VFSFile(name=name, date=node.mtime, access=access_flags, size=node.size, path=node.path)

        current_dir.items.append(obj)

    return root


# with zipfile.ZipFile("ExampleDir/archive.zip", 'r') as zip_archive:
#     data = zip_archive.infolist()
# build_root_from_zip_info(data).print_recursion()


# for i in data:
#     print(i)
#     print(i.comment)
#     print(i.CRC)
#     print(i.extra)
#     print(i.internal_attr)
#     print(i.reserved)
#     print(i.external_attr)
#     print(i.internal_attr)
#
#     hi = i.external_attr >> 16
#     if hi:
#         print("Access", stat.filemode(hi))
#     print("=-=-=-=-=-=-=-=-=-=-=-=-=")


# with tarfile.TarFile.open('ExampleDir/archive.tar') as tar:
#     infos = tar.getmembers()
#     added_paths = set()
#     data = []
#     for inf in infos:
#         if inf.path not in added_paths:
#             data.append(inf)
#             added_paths.add(inf.path)
#         inf: tarfile.TarInfo
#         print(inf.name)
#         print(inf.path)
#         print(inf.size)
#         print(inf.type)
#         print(inf.gid)
#         print(inf.mode)
#         print("MODE: ", oct(inf.mode))
#         print(inf.get_info())
#
#
# build_root_from_tar_info(data).print_recursion()




