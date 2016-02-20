import os

__version__ = "1.0.5"

if os.name == "nt":
    from start_jupyter_cm.windows import (add_jupyter_here,
                                          remove_jupyter_here)
elif os.environ.get('KDE_FULL_SESSION') == 'true':
    # Running KDE
    from start_jupyter_cm.kde import (add_jupyter_here,
                                      remove_jupyter_here)
else:
    # Default fallback is gnome
    from start_jupyter_cm.gnome import (add_jupyter_here,
                                        remove_jupyter_here)


def _add():
    add_jupyter_here()


def _remove():
    remove_jupyter_here()
