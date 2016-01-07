import os


if os.name == "nt":
    from start_jupyter_cm.windows import (install_jupyter_here,
                                          uninstall_jupyter_here)
else:
    from start_jupyter_cm.gnome import (install_jupyter_here,
                                        uninstall_jupyter_here)
