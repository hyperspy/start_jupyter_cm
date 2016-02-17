import os

__version__ = "1.0.2"

if os.name == "nt":
    from start_jupyter_cm.windows import (add_jupyter_here,
                                          remove_jupyter_here)
else:
    from start_jupyter_cm.gnome import (add_jupyter_here,
                                        remove_jupyter_here)
