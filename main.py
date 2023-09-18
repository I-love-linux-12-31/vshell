import argparse
import os.path
import sys

import Lib.vfs
from Lib.argparse import Command
from Lib.utils import *


def main(path: str, mode: str = "auto", script: str = None):
    if script is not None and os.path.exists(script):
        scriptmode = True
        f = open(script, "rt", encoding="utf-8")
        sys.stdin = f
    else:
        scriptmode = False

    Lib.vfs.init(path, mode)
    cmd = ""
    while cmd.upper() != "EXIT":
        if not scriptmode:
            cmd = input(f"\033[34mroot@vshell:\033[32m{Lib.vfs.current_dir}\033[0m$")
        else:
            cmd = input()

        if not cmd.strip():
            continue

        parsed_command = Command(cmd)

        try:

            match parsed_command.cmd:
                case "ls":
                    parsed_command(ls)
                case "pwd":
                    parsed_command(pwd)
                case "cd":
                    parsed_command(cd)
                case "cat":
                    parsed_command(cat)
                case "exit":
                    pass
                case "EXIT":
                    pass
                case _:
                    print("\033[33mCommand not found!\033[0m")
        except EOFError:
            return
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f"\033[31mError:\033[0m {e.__class__.__name__} : {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VShell - cross platform linux shell emulator.'
                                                 ' App works in virtual filesystem inside a archives (tar, zip)')
    parser.add_argument('--archive', type=str, help='Path to archive.', default="ExampleDir/archive.tar")
    parser.add_argument('--script', type=str, help='Path to archive.')
    args = parser.parse_args()
    main(path=args.archive, script=args.script)
    # todo: script must be in archive !!! not by fs path! By vfs path!
