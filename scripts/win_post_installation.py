import sys
import start_jupyter_cm

if sys.argv[1] == '-install':
    start_jupyter_cm.add_jupyter_here()
else:
    start_jupyter_cm.remove_jupyter_here()
