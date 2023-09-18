import Lib.vfs


def echo(*args, **modes):
    res = ""
    if len(args) > 0:
        res = args[0]

    print(res)
