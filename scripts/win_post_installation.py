import sys
import start_jupyter_cm

if sys.argv[1] == '-install':
    start_jupyter_cm.install_jupyter_here()
else:
    start_jupyter_cm.uninstall_jupyter_here()
