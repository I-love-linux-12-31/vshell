import Lib.vfs


def ls(*args, **modes):
    path = modes.setdefault("path", './')
    if len(args) > 0 and not args[0].startswith("-"):
        path = args[0]
    default = dict()
    default["color"] = True
    default["list"] = False
    default["all"] = False
    default["human_readable"] = False

    if "--list" in args or "-l" in args:
        modes["list"] = True

    if "--all" in args or "-a" in args:
        modes["all"] = True

    path = Lib.vfs.simplify_path(path)
    target = Lib.vfs.get_object_by_path(path)
    if isinstance(target, Lib.vfs.VFSDirectory) or isinstance(target, Lib.vfs.VFSRoot):
        if not modes.setdefault("list", default["list"]):
            if not modes.setdefault("all", default["all"]):
                print(*[i.name for i in target.items if not i.name.startswith('.')])
            else:
                print(*[i.name for i in target.items])
        else:
            if not modes.setdefault("all", default["all"]):
                print(*[i.get_ls_string() for i in target.items if not i.name.startswith('.')], sep="\n")
            else:
                print(*[i.get_ls_string() for i in target.items], sep="\n")
    elif target is None:
        print("\033[31mError!\033[0m path is invalid!")
    else:
        print("\033[31mError!\033[0m it is not a directory!")
