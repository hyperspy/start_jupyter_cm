import os, sys
import stat
from subprocess import call
import shutil

from .utils import get_environment_label

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

def check_supported_file_manager(manager_file_path):
    if len(manager_file_path) == 0:
        print("Nothing done. Currently only 'Nautilus' and 'Caja' are "
              "supported file manager.")
        return False
    return True


def get_file_manager_config(file_manager=None):
    file_manager_config = {}
    
    if shutil.which("nautilus"):
        file_manager_config['Nautilus'] = os.path.expanduser("~/.local/share/nautilus")
    if shutil.which("caja"):
        file_manager_config['Caja'] = os.path.expanduser("~/.config/caja")

    if file_manager is not None:
        if file_manager not in file_manager_config.keys():
            print("File manager '%s' not installed or not supported." % file_manager)
            return {}
        return {file_manager:file_manager_config[file_manager]}
    else:
        return file_manager_config


def add_jupyter_here(file_manager=None):
    manager_config_path = get_file_manager_config(file_manager)
    if not check_supported_file_manager(manager_config_path):
        return

    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.png'),
             'notebook': os.path.join(logo_path, 'jupyter.png'),
             'lab': os.path.join(logo_path, 'jupyter.png')}

    python_exec = shutil.which("python")

    for name, path in manager_config_path.items():
        print("File manager: %s" %name)
        scripts_folder_path = os.path.join(path, "scripts")
    
        if not os.path.exists(scripts_folder_path):
            os.makedirs(scripts_folder_path)
        for terminal in ["qtconsole", "notebook", "lab"]:
            script_path = os.path.join(scripts_folder_path, "Jupyter %s here%s" % (
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


def remove_jupyter_here(file_manager=None):
    manager_config_path = get_file_manager_config(file_manager)
    if not check_supported_file_manager(manager_config_path):
        return

    for name, path in manager_config_path.items():
        print("File manager: %s" %name)
        scripts_folder_path = os.path.join(path, "scripts")
        for terminal in ["qtconsole", "notebook", "lab"]:
            script_path = os.path.join(scripts_folder_path, "Jupyter %s here%s" %(
                    terminal, CONDA_ENV_LABEL))
            if os.path.exists(script_path):
                os.remove(script_path)
                print("Jupyter %s here%s removed." % (terminal, CONDA_ENV_LABEL))
