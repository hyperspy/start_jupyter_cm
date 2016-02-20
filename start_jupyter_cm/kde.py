import os
import stat
from shutil import copy

homedir = os.environ['HOME']
KPATH = os.path.join(homedir, ".local/share/kservices5/ServiceMenus")

script = \
    """#!/usr/bin/python

import sys
import os.path
import subprocess

folders = [path for path in sys.argv[1:] if os.path.isdir(path)]
any_file_selected = len(folders) < len(sys.argv[1:])
if any_file_selected:
    subprocess.Popen(["jupyter-%s"])
for folder in folders:
    os.chdir(folder)
    subprocess.Popen(["jupyter-%s"])
    os.chdir("..")

"""


def get_script_file(terminal):
    """
    Returns the contents of a script file that will launch Jupyter
    in a certain mode

    Parameters
    ----------
    terminal: str
        Either 'notebook' or 'qtconsole'
    """
    if terminal == 'qtconsole':
        terminal += '-py2'

    script_file = \
        ("#!/usr/bin/python\n"
         "\n"
         "import sys\n"
         "import os.path\n"
         "import subprocess\n"
         "\n"
         "folders = [path for path in sys.argv[1:] if os.path.isdir(path)]\n"
         "any_file_selected = len(folders) < len(sys.argv[1:])\n"
         "if any_file_selected:\n"
         "    subprocess.Popen([\"jupyter-{0}\"])\n"
         "for folder in folders:\n"
         "    os.chdir(folder)\n"
         "    subprocess.Popen([\"jupyter-{0}\"])\n"
         "    os.chdir(\"..\")\n"
         "\n").format(terminal)
    return script_file


def get_desktop_file(terminal):
    """
    Returns the contents of a desktop file that will launch Jupyter
    in a certain mode

    Parameters
    ----------
    terminal: str
        Either 'notebook' or 'qtconsole'
    """
    desktop_file = \
        ("\n"
         "[Desktop Action jupyter-{1}]\n"
         "Exec={0}/.local/share/kservices5/ServiceMenus/"
         "Jupyter_{1}_here.sh %f\n"
         "Icon={0}/.local/share/kservices5/ServiceMenus/jupyter-{1}.png\n"
         "Name=Jupyter {2} here\n"
         "\n"
         "[Desktop Entry]\n"
         "Actions=jupyter-{1};\n"
         "MimeType=\n"
         "ServiceTypes=inode/directory\n"
         "Type=Service\n"
         "X-KDE-ServiceTypes=KonqPopupMenu/Plugin,"
         "inode/directory,all/all,all/allfiles\n"
         "").format(homedir, terminal, terminal.capitalize())
    return desktop_file


def add_jupyter_here():
    if not os.path.exists(KPATH):
        os.makedirs(KPATH)

    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.png'),
             'notebook': os.path.join(logo_path, 'jupyter.png')}
    for terminal in ["qtconsole", "notebook"]:
        script_path = os.path.join(KPATH,
                                   "Jupyter_{}_here.sh".format(terminal))
        if not os.path.exists(script_path):
            copy(logos[terminal], KPATH)
            with open(script_path, "w") as f:
                f.write(get_script_file(terminal))
            st = os.stat(script_path)
            os.chmod(script_path, st.st_mode | stat.S_IEXEC)
            print('Jupyter {} (KDE) here created.'.format(terminal))

        jupyter_logo = os.path.join(KPATH, 'jupyter.png')
        if terminal == "notebook" and os.path.exists(jupyter_logo):
            os.rename(jupyter_logo, os.path.join(KPATH,
                                                 'jupyter-notebook.png'))

        desktop_path = os.path.join(KPATH,
                                    "jupyter_{}.desktop".format(terminal))
        if not os.path.exists(desktop_path):
            # print get_desktop_file(terminal)
            with open(desktop_path, "w") as f:
                f.write(get_desktop_file(terminal))


def remove_jupyter_here():
    for terminal in ["qtconsole", "notebook"]:
        script_path = os.path.join(KPATH,
                                   "Jupyter_{}_here.sh".format(terminal))
        desktop_path = os.path.join(KPATH,
                                    "jupyter_{}.desktop".format(terminal))
        if os.path.exists(script_path):
            os.remove(script_path)
            print("Jupyter {} (KDE) here removed.".format(terminal))
        if os.path.exists(desktop_path):
            os.remove(desktop_path)

    try:
        os.remove(os.path.join(KPATH, 'jupyter-qtconsole.png'))
        os.remove(os.path.join(KPATH, 'jupyter-notebook.png'))
        os.remove(os.path.join(KPATH, 'jupyter.png'))
    except OSError, _:
        pass
