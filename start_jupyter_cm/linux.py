import os
import sys
import stat
from subprocess import call
import shutil

from .utils import get_environment_label

# Logic to detect desktop environments on Linux:
NPATH = os.path.expanduser("~/.local/share/nautilus")
# User directories might not exist by default in KDE so detect root install:
KPATH = "/usr/share/kservices5/ServiceMenus"
no_supported_DE = True

if os.path.isdir(NPATH):
    GNOME = True
    no_supported_DE = False
if os.path.isdir(KPATH):
    KDE = True
    no_supported_DE = False

if GNOME:
    SPATH = os.path.join(NPATH, "scripts")

if KDE:
    KPATH = os.path.expanduser("~/.local/share/kservices5/ServiceMenus")

if no_supported_DE:
    raise EnvironmentError('start_jupyter_cm only supports Gnome (+ Nautilus '
                           'file manager) and KDE (+ Dolphin file manager) '
                           'desktop environments on Linux, and neither was '
                           'detected. Nothing has been installed.')


# Get python path and anaconda environment:
PATH = "{}/bin".format(sys.exec_prefix)
CONDA_ENV_LABEL = get_environment_label()

script = \
    """#!/usr/bin/python

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


def get_desktop_file(app, logo):
    """
    Returns the contents of a desktop file that will launch Jupyter
    in a certain mode. Required since KDE uses .desktop files instead of
    just scripts.

    Parameters
    ----------
    app : str
        Either 'notebook', 'qtconsole', or 'lab'
    logo : str
        Path to the logo file to use for the .desktop file
    """
    desktop_file = \
        ("\n"
         "[Desktop Action jupyter-{1}]\n"
         "Exec='{0}/.local/share/kservices5/ServiceMenus/"
         "Jupyter_{1}_here{2}' %f\n"
         "Icon={3}\n"
         "Name=Jupyter {4}{2} here\n"
         "\n"
         "[Desktop Entry]\n"
         "Actions=jupyter-{1};\n"
         "MimeType=\n"
         "ServiceTypes=inode/directory\n"
         "Type=Service\n"
         "X-KDE-ServiceTypes=KonqPopupMenu/Plugin,"
         "inode/directory,all/all,all/allfiles\n"
         "").format(os.environ['HOME'], app, CONDA_ENV_LABEL,
                    logo, app.capitalize())
    return desktop_file


def add_jupyter_here():
    # logo paths are common to Gnome and KDE:
    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.png'),
             'notebook': os.path.join(logo_path, 'jupyter.png'),
             'lab': os.path.join(logo_path, 'jupyter.png')}

    if GNOME:
        if not os.path.exists(SPATH):
            os.makedirs(SPATH)

        for terminal in ["qtconsole", "notebook", "lab"]:
            script_path = os.path.join(SPATH, "Jupyter %s here%s" % (
                    terminal, CONDA_ENV_LABEL))
            if (not os.path.exists(script_path) and
                    shutil.which("jupyter-%s" % terminal)):
                with open(script_path, "w") as f:
                    f.write(script % (PATH, terminal, PATH, terminal))
                st = os.stat(script_path)
                os.chmod(script_path, st.st_mode | stat.S_IEXEC)
                call(['gio', 'set', '-t', 'string', '%s' % script_path,
                      'metadata::custom-icon', 'file://%s' % logos[terminal]])
                print('Gnome: Jupyter %s here%s created.' %
                      (terminal, CONDA_ENV_LABEL))

    if KDE:
        if not os.path.exists(KPATH):
            os.mkdir(KPATH)
        for terminal in ["qtconsole", "notebook", "lab"]:
            script_path = os.path.join(KPATH, "Jupyter_{}_here{}"
                                              "".format(terminal,
                                                        CONDA_ENV_LABEL))
            if (not os.path.exists(script_path)
                    and shutil.which("jupyter-{}".format(terminal))):
                with open(script_path, "w") as f:
                    f.write(script % (PATH, terminal, PATH, terminal))
                st = os.stat(script_path)
                os.chmod(script_path, st.st_mode | stat.S_IEXEC)

                print("  KDE: Jupyter {} here{} script created."
                      "".format(terminal, CONDA_ENV_LABEL))

            desktop_path = os.path.join(KPATH,
                                        "jupyter_{}{}.desktop"
                                        "".format(terminal, CONDA_ENV_LABEL))
            if not os.path.exists(desktop_path):
                print('  KDE: Jupyter {} here{} desktop file '
                      'created.'.format(terminal, CONDA_ENV_LABEL))
                with open(desktop_path, "w") as f:
                    f.write(get_desktop_file(terminal, logos[terminal]))


def remove_jupyter_here():
    for terminal in ["qtconsole", "notebook", "lab"]:
        if GNOME:
            script_path = os.path.join(SPATH,
                                       "Jupyter {} here{}"
                                       "".format(terminal, CONDA_ENV_LABEL))
            if os.path.exists(script_path):
                os.remove(script_path)
                print("Gnome: Jupyter {} here{} removed."
                      "".format(terminal, CONDA_ENV_LABEL))

        if KDE:
            script_path = os.path.join(KPATH,
                                       "Jupyter_{}_here{}"
                                       "".format(terminal, CONDA_ENV_LABEL))
            if os.path.exists(script_path):
                os.remove(script_path)
                print("  KDE: Jupyter {} here{} removed."
                      "".format(terminal, CONDA_ENV_LABEL))

            desktop_path = os.path.join(KPATH,
                                        "jupyter_{}{}.desktop"
                                        "".format(terminal, CONDA_ENV_LABEL))
            if os.path.exists(desktop_path):
                os.remove(desktop_path)
                print("  KDE: jupyter_{}{}.desktop removed."
                      "".format(terminal, CONDA_ENV_LABEL))
