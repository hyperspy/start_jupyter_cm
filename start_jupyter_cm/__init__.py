import os

__version__ = "1.3.0"

if os.name == "nt":
    from start_jupyter_cm.windows import (add_jupyter_here,
                                          remove_jupyter_here)
else:
    from start_jupyter_cm.gnome import (add_jupyter_here,
                                        remove_jupyter_here)


def _add():
    add_jupyter_here()


def _remove():
    remove_jupyter_here()
