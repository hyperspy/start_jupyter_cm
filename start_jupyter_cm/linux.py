import os, sys
import stat
from subprocess import call
import shutil
import pathlib

from .utils import get_environment_label


PATH = f"{sys.exec_prefix}/bin"
CONDA_ENV_LABEL = get_environment_label()


def get_script(python_exec, path, terminal):
    script = \
f"""#!{python_exec}

import sys
import os.path
import subprocess

folders = [path for path in sys.argv[1:] if os.path.isdir(path)]
any_file_selected = len(folders) < len(sys.argv[1:])
if any_file_selected or len(folders) == 0:
    subprocess.Popen(["{path}/jupyter-{terminal}"])
for folder in folders:
    os.chdir(folder)
    subprocess.Popen(["{path}/jupyter-{terminal}"])
    os.chdir("..")

"""
    return script


def get_desktop(path, terminal, logo, shortcut_name):
    """
    Returns the contents of a desktop file that will launch Jupyter
    from the current environment.

    Parameters
    ----------
    path : str
        'bin' path of the python distribution
    terminal : str
        Either 'notebook', 'qtconsole', or 'lab'
    logo : str
        Path to the logo file to use for the .desktop file
    shortcut_name : str
        Name of the shortcut.
    """
    exec_ = os.path.join(path, f'jupyter-{terminal}')
    desktop_file = \
f"""\n
[Desktop Action {shortcut_name}]\n
Exec='{exec_}'\n
Icon={logo}\n
Name={shortcut_name}\n
\n
[Desktop Entry]\n
Actions={shortcut_name};\n
MimeType=\n
ServiceTypes=inode/directory\n
Type=Service\n
X-KDE-ServiceTypes=KonqPopupMenu/Plugin,
inode/directory,all/all,all/allfiles\n
"""
    return desktop_file


def get_nemo_action(path, terminal, logo, shortcut_name):
    """
    Returns the contents of a nemo action file that will launch Jupyter
    from the current environment.
    See https://github.com/linuxmint/nemo/blob/master/files/usr/share/nemo/actions/sample.nemo_action

    Parameters
    ----------
    path : str
        'bin' path of the python distribution
    terminal : str
        Either 'notebook', 'qtconsole', or 'lab'
    logo : str
        Path to the logo file to use for the .desktop file
    shortcut_name : str
        Name of the shortcut.
    """
    exec_ = os.path.join(path, f'jupyter-{terminal}')
    nemo_action_file = \
f"""[Nemo Action]
Active=true
Name={shortcut_name}
Comment=Start a {shortcut_name}.
Exec=sh -c 'cd %F && {exec_}'
Icon={logo}
Selection=any
Extensions=any
# https://github.com/jupyter/qtconsole/blob/master/examples/jupyter-qtconsole.desktop
# Icon-Name=network-idle
Quote=double
"""
    return nemo_action_file


def check_supported_file_manager(manager_file_path):
    if len(manager_file_path) == 0:
        print("Nothing done. Currently only 'Nautilus', 'Caja' and 'Dolphin' "
              "are supported file manager.")
        return False
    return True


def get_file_manager_config(file_manager=None):
    file_manager_config = {}

    if shutil.which("nautilus"):
        file_manager_config['nautilus'] = os.path.expanduser("~/.local/share/nautilus/scripts")
    if shutil.which("caja"):
        file_manager_config['caja'] = os.path.expanduser("~/.config/caja/scripts")
    if shutil.which("dolphin"):
        file_manager_config['dolphin'] = os.path.expanduser("~/.local/share/kservices5/ServiceMenus")
    if shutil.which("nemo"):
        file_manager_config['nemo'] = os.path.expanduser("~/.local/share/nemo/actions/")

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

    for name, scripts_folder_path in manager_config_path.items():
        print(f"File manager: {name}")

        if not os.path.exists(scripts_folder_path):
            # In case the parent folder doesn't exist
            pathlib.Path(scripts_folder_path).mkdir(parents=True)

        for terminal in ["qtconsole", "notebook", "lab"]:
            shortcut_name = f"Jupyter {terminal.capitalize()} here{CONDA_ENV_LABEL}"
            if name == 'dolphin':
                script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.desktop")
                script = get_desktop(PATH, terminal, logos[terminal], shortcut_name)
            elif name == 'nemo':
                script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.nemo_action")
                script = get_nemo_action(PATH, terminal, logos[terminal], shortcut_name)
            else:
                script_path = os.path.join(scripts_folder_path, shortcut_name)
                script = get_script(python_exec, PATH, terminal)

            # Check that we are getting jupyter from the current environment
            executable_path = shutil.which(f"jupyter-{terminal}")
            if executable_path and PATH in executable_path:
                with open(script_path, "w") as f:
                    f.write(script)
                st = os.stat(script_path)
                os.chmod(script_path, st.st_mode | stat.S_IEXEC)
                # For nautilus and caja, we need to call gio
                if name in ['nautilus', 'caja'] and shutil.which("gio"):
                    # Call it only if available in the system
                    call(['gio', 'set', '-t', 'string', script_path,
                          'metadata::custom-icon', f'file://{logos[terminal]}'])
                print(f'{shortcut_name} created.')


def remove_jupyter_here(file_manager=None):
    manager_config_path = get_file_manager_config(file_manager)
    if not check_supported_file_manager(manager_config_path):
        return

    for name, scripts_folder_path in manager_config_path.items():
        print(f"File manager: {name}")

        for terminal in ["qtconsole", "notebook", "lab"]:
            shortcut_name = f"Jupyter {terminal.capitalize()} here{CONDA_ENV_LABEL}"
            if name == 'dolphin':
                script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.desktop")
            elif name == 'nemo':
                script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.nemo_action")
            else:
                script_path = os.path.join(scripts_folder_path, shortcut_name)

            if os.path.exists(script_path):
                os.remove(script_path)
                print(f"{shortcut_name} removed.")
