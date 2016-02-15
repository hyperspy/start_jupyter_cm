import os


if os.name == "nt":
    from start_jupyter_cm.windows import (add_jupyter_here,
                                          remove_jupyter_here)
else:
    from start_jupyter_cm.gnome import (add_jupyter_here,
                                        remove_jupyter_here)
