import os, sys
import stat
from subprocess import call
import shutil

from .utils import get_environment_label

MANAGER_CONFIG_PATH = ""

if shutil.which("nautilus"):
    MANAGER_CONFIG_PATH = os.path.expanduser("~/.local/share/nautilus")
if shutil.which("caja"):
    MANAGER_CONFIG_PATH = os.path.expanduser("~/.config/caja")

if MANAGER_CONFIG_PATH == "":
    print("Only 'nautilus' and 'caja' are supported "
                              "file manager on linux.")

SPATH = os.path.join(MANAGER_CONFIG_PATH, "scripts")
PATH = "%s/bin"%sys.exec_prefix
CONDA_ENV_LABEL = get_environment_label()


script = \
"""#!%s

import sys
import os.path
import subprocess

folders = [path for path in sys.argv[1:] if os.path.isdir(path)]
any_file_selected = len(folders) < len(sys.argv[1:])
if any_file_selected:
    subprocess.Popen(["%s/jupyter-%s"])
for folder in folders:
    os.chdir(folder)
    subprocess.Popen(["%s/jupyter-%s"])
    os.chdir("..")

"""

def check_supported_file_manager():
    if not os.path.exists(MANAGER_CONFIG_PATH):
        print("Nothing done. Currently only 'Nautilus' and 'Caja' are "
              "supported file manager.")
        return False
    return True


def add_jupyter_here():
    if not check_supported_file_manager:
        return
    
    if not os.path.exists(SPATH):
        os.makedirs(SPATH)

    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.png'),
             'notebook': os.path.join(logo_path, 'jupyter.png'),
             'lab': os.path.join(logo_path, 'jupyter.png')}

    python_exec = shutil.which("python")

    for terminal in ["qtconsole", "notebook", "lab"]:
        script_path = os.path.join(SPATH, "Jupyter %s here%s" % (
                terminal, CONDA_ENV_LABEL))
        if (not os.path.exists(script_path) and
            shutil.which("jupyter-%s" % terminal)):
            with open(script_path, "w") as f:
                f.write(script % (python_exec, PATH, terminal, PATH, terminal))
            st = os.stat(script_path)
            os.chmod(script_path, st.st_mode | stat.S_IEXEC)
            call(['gio', 'set', '-t', 'string', '%s' % script_path,
                  'metadata::custom-icon', 'file://%s' % logos[terminal]])
            print('Jupyter %s here%s created.' % (terminal, CONDA_ENV_LABEL))


def remove_jupyter_here():
    if not check_supported_file_manager:
        return
    for terminal in ["qtconsole", "notebook", "lab"]:
        script_path = os.path.join(SPATH, "Jupyter %s here%s" %(
                terminal, CONDA_ENV_LABEL))
        if os.path.exists(script_path):
            os.remove(script_path)
            print("Jupyter %s here%s removed." % (terminal, CONDA_ENV_LABEL))
