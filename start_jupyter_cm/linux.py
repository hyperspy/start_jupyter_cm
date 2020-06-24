import os, sys
import stat
from subprocess import call
import shutil

from .utils import get_environment_label


PATH = f"{sys.exec_prefix}/bin"
CONDA_ENV_LABEL = get_environment_label()


def get_script(python_exec, PATH, terminal):
    script = \
f"""#!{python_exec}

import sys
import os.path
import subprocess

folders = [path for path in sys.argv[1:] if os.path.isdir(path)]
any_file_selected = len(folders) < len(sys.argv[1:])
if any_file_selected:
    subprocess.Popen(["{PATH}/jupyter-{terminal}"])
for folder in folders:
    os.chdir(folder)
    subprocess.Popen(["{PATH}/jupyter-{terminal}"])
    os.chdir("..")

"""
    return script


def check_supported_file_manager(manager_file_path):
    if len(manager_file_path) == 0:
        print("Nothing done. Currently only 'Nautilus' and 'Caja' are "
              "supported file manager.")
        return False
    return True


def get_file_manager_config(file_manager=None):
    file_manager_config = {}

    if shutil.which("nautilus"):
        file_manager_config['nautilus'] = os.path.expanduser("~/.local/share/nautilus")
    if shutil.which("caja"):
        file_manager_config['caja'] = os.path.expanduser("~/.config/caja")

    if file_manager is not None:
        if file_manager not in file_manager_config.keys():
            print(f"File manager '{file_manager}' not installed or not supported.")
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
        print(f"File manager: {name}")
        scripts_folder_path = os.path.join(path, "scripts")
        if not os.path.exists(scripts_folder_path):
            os.makedirs(scripts_folder_path)

        for terminal in ["qtconsole", "notebook", "lab"]:
            shortcut_name = f"Jupyter {terminal} here{CONDA_ENV_LABEL}"
            script_path = os.path.join(scripts_folder_path, shortcut_name)
            if (not os.path.exists(script_path) and
                shutil.which(f"jupyter-{terminal}")):
                with open(script_path, "w") as f:
                    f.write(get_script(python_exec, PATH, terminal))
                st = os.stat(script_path)
                os.chmod(script_path, st.st_mode | stat.S_IEXEC)
                call(['gio', 'set', '-t', 'string', script_path,
                      'metadata::custom-icon', f'file://{logos[terminal]}'])
                print(f'{shortcut_name} created.')


def remove_jupyter_here(file_manager=None):
    manager_config_path = get_file_manager_config(file_manager)
    if not check_supported_file_manager(manager_config_path):
        return

    for name, path in manager_config_path.items():
        print(f"File manager: {name}")
        scripts_folder_path = os.path.join(path, "scripts")

        for terminal in ["qtconsole", "notebook", "lab"]:
            shortcut_name = f"Jupyter {terminal} here{CONDA_ENV_LABEL}"
            script_path = os.path.join(scripts_folder_path, shortcut_name)
            if os.path.exists(script_path):
                os.remove(script_path)
                print(f"{shortcut_name} removed.")
