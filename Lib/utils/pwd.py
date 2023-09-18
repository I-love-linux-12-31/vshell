import Lib.vfs


def pwd(*args, **kwargs):
    print(Lib.vfs.current_dir)
