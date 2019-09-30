import os, sys
import shutil

from .utils import get_environment_label

NPATH = os.path.expanduser("~/Library/Services/")
PATH = "%s/bin"%sys.exec_prefix
CONDA_ENV_LABEL = get_environment_label()



def add_jupyter_here():
    if not os.path.exists(NPATH):
        print("Nothing done. User Library is unavailable, are you sure this is OSX?")
        return

    workflow_path = os.path.expandvars(os.path.join(
                os.path.dirname(__file__), 'prototype.workflow/Contents'))
    docu_prototype = os.path.join(workflow_path,'document.wflow')
    info_prototype = os.path.join(workflow_path,'Info.plist')
    with open(docu_prototype, "r") as f:
        document = f.read()
    with open(info_prototype, "r") as f:
        info = f.read()

    for terminal in ["qtconsole", "notebook", "lab"]:
        script_dir = os.path.join(NPATH, "Jupyter %s here%s.workflow/Contents" % (
                terminal, CONDA_ENV_LABEL))
        if (not os.path.exists(script_dir) and
                shutil.which("jupyter-%s" % terminal)):
            os.makedirs(script_dir)
            document_path = os.path.join(script_dir, "document.wflow")
            info_path = os.path.join(script_dir, "Info.plist")
                
            if not os.path.exists(document_path):
                with open(document_path, "w") as f:
                    f.write(document % (PATH, terminal, PATH, terminal))
            if not os.path.exists(info_path):
                with open(info_path, "w") as f:
                    f.write(info % (terminal, CONDA_ENV_LABEL))
            print('Jupyter %s here%s created.' % (terminal, CONDA_ENV_LABEL))



def remove_jupyter_here():
    for terminal in ["qtconsole", "notebook", "lab"]:
        script_path = os.path.join(NPATH, "Jupyter %s here%s.workflow" %(
                terminal, CONDA_ENV_LABEL))
        if os.path.exists(script_path):
            shutil.rmtree(script_path)
            print("Jupyter %s here%s removed." % (terminal, CONDA_ENV_LABEL))



'''
Guide for building this script using Automator.

This guide was originally based on this article: https://davidwalsh.name/mac-context-menu

1) Start Automator (either through the Applications folder, or spotlight search)

2) Open the "File" dropdown menu, and select "New"

3) Choose the "Quick Action" document type (this is represented by the cog icon, 
and used to be called "Service")

4) In the "Library" menu on the left chose "Utilities", and then double-click on
"Run Shell Script" in the menu 2nd on the left. This will open a "Run Shell Script" 
panel in the right pane.

5) Using the dropdown menus in the uppermost panel in the right pane set the workflow to
receive current "files or folders" in "finder".

6) In top-right corner of the "Run Shell Script" panel, set Pass Input "as arguments".

7) Write Bash script, using this template (substitute for the anaconda install path, and 
swap out jupyter-notebook for your python application of choice):
#!/bin/bash
if [[ -d $1 ]] ; then
    cd "$1"
    current_file="None"
else
    current_path=$(dirname "$1")
    current_file=$(basename "$1")
    cd "$current_path"
fi

if [[ $current_file == *.ipynb ]] ; then
    [path to anaconda install]/bin/jupyter-notebook "$current_file"
else
    [path to anaconda install]/bin/jupyter-notebook
fi

8) Save the script (using a descriptive name), and test it as described in the README file.
'''

