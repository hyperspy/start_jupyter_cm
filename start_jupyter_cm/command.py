import argparse
import os

from start_jupyter_cm import __version__

parser = argparse.ArgumentParser(
    description='Add or remove context menu entries to start Jupyter applications in a given directory')
parser.add_argument('--remove', action="store_true", help='remove the entries')
parser.add_argument('-f', '--file_manager', action="store", help='specific a file manager', choices=['nautilus', 'caja', 'dolphin', 'nemo'])
parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))

args = parser.parse_args()


def _run():
    global args
    params = []
    if os.name == "nt":
        from start_jupyter_cm.windows import (add_jupyter_here,
                                              remove_jupyter_here)
    elif os.uname().sysname == "Darwin":
        from start_jupyter_cm.macos import (add_jupyter_here,
                                            remove_jupyter_here)
    else:
        from start_jupyter_cm.linux import (add_jupyter_here,
                                            remove_jupyter_here)
        if args.file_manager:
            params.append(args.file_manager)

    if args.remove:
        remove_jupyter_here(*params)
    else:
        add_jupyter_here(*params)
