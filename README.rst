start\_jupyter\_cm
==================

|pypi_version|_  |python_version|_ |conda-forge|_ |travis|_ |appveyor|_

.. |pypi_version| image:: https://img.shields.io/pypi/v/start-jupyter-cm.svg?style=flat
.. _pypi_version: https://pypi.python.org/pypi/start-jupyter-cm

.. |python_version| image:: https://img.shields.io/pypi/pyversions/start-jupyter-cm.svg?style=flat
.. _python_version: https://pypi.python.org/pypi/start-jupyter-cm

.. |conda-forge| image:: https://img.shields.io/conda/pn/conda-forge/start_jupyter_cm?label=conda-forge
.. _conda-forge: https://anaconda.org/conda-forge/start_jupyter_cm

.. |travis| image:: https://img.shields.io/travis/hyperspy/start_jupyter_cm?label=Travis
.. _travis: https://travis-ci.org/github/hyperspy/start_jupyter_cm

.. |appveyor| image:: https://img.shields.io/appveyor/build/hyperspy/start-jupyter-cm?label=Appveyor
.. _appveyor: https://ci.appveyor.com/project/hyperspy/start-jupyter-cm


Description
-----------

Add entries to start the `Jupyter Notebook <https://jupyter-notebook.readthedocs.io>`__,
`Jupyter QtConsole <https://qtconsole.readthedocs.io>`__ or
`JupyterLab <https://jupyterlab.readthedocs.io>`__ from the file
manager context menu. This offers a convenient way of starting Jupyter
in a folder. Currently it only supports Microsoft Windows, GNOME (and
its many derivatives), and macOS. Contributions to support other OSs/desktop
environments are highly welcome.

`WinPython <http://winpython.github.io>`__ and
`Anaconda <https://www.anaconda.com/distribution>`__/
`Miniconda <https://docs.conda.io/en/latest/miniconda.html>`__ distributions
are supported. If run from a conda environment other than `root`, the name of
the environment will be specified in brackets in the context menu name.

Microsoft Windows
~~~~~~~~~~~~~~~~~

.. figure:: https://github.com/hyperspy/start_jupyter_cm/raw/master/images/jupyter_cm_windows.png
   :alt: Jupyter context menu entries in windows
   :width: 250px

   Jupyter context menu entries in windows.


In addition to starting the QtConsole, the Jupyter Notebook or the Jupyter Lab,
and launching the default browser, in Microsoft Windows the process runs from
a terminal. Closing the terminal closes the QtConsole or the Jupyter server.
Single and all users installations are supported, see installation instructions below.

Linux
~~~~~

On linux, the supported file managers are: Nautilus (GNOME), Caja (MATE), Dolphin (KDE) and Nemo (Cinnamon).
With Nautilus and Caja, the shortcut will appear in the *Scripts* menu and with
Dolphin, it will appear in the *Actions* menu.

.. figure:: https://github.com/hyperspy/start_jupyter_cm/raw/master/images/jupyter_cm_gnome.png
   :alt: Jupyter context menu entries in Nautilus
   :width: 450px

   Jupyter context menu entries on Linux (Nautilus).


When selecting multiple folders, one instance of Jupyter
QtConsole/notebook/lab opens in each of the selected folders. Selecting a
file starts Jupyter in the file directory.

Note that on Linux the processes run in the background: to stop the jupyter
notebook or lab, don't forget to exit using the *quit* button - only closing
the tab will not stop the jupyter server. Alternatively, `nbmanager <https://github.com/takluyver/nbmanager>`__
can discover all running servers and shut them down using via an UI.


macOS
~~~~~

.. figure:: https://github.com/hyperspy/start_jupyter_cm/raw/master/images/jupyter_cm_macos.png
   :alt: Jupyter context menu entries in macOS
   :width: 450px

   Jupyter context menu entries on macOS.


The context menu is only available when an object (folder or file) is
selected in Finder. The Jupyter options will be available from the
"Services" section of the menu. If a folder is selected then an instance of
Jupyter QTConsole/notebook/lab opens in the selected folder. If a file
is selected then Jupyter is started in the file directory. If the
file is a jupyter notebook (\*.ipynb), then selecting Jupyter notebook/lab
will open the file in that program; Jupyter QtConsole will still only
open in the file directory.

As the processes are opened through a shell script in Automator, a spinning
cog will be visible in the menu bar when the processes are running. Once you
have finished with the server then manually kill the process via the
drop-down menu from this spinning cog.

The launchers have been tested on macOS Mojave (10.14.6).

Installation instructions
-------------------------

Install from pypi using pip:

.. code:: bash

    $ pip install start_jupyter_cm

Or install from conda-forge channel using conda (in a Anaconda/Miniconda distribution):

.. code:: bash

    $ conda install -c conda-forge start_jupyter_cm

Usage
-----

Create context menu shortcut(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installation, enable the context menu entries from a terminal as follows:

.. code:: bash

    $ start_jupyter_cm

On Microscoft Windows, the administrator rights are required to add the
entry for all users, otherwise the entries will be added only for the
current user. In GNOME and OSX only for the current user.

Remove context menu shortcut(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove the context menu entries execute the following in a terminal:

.. code::

    $ start_jupyter_cm --remove

Also, be aware that, uninstalling the package does not
remove the context menu entries. If you are left with the context menu
entries after uninstalling ``start_jupyter_cm``, reinstall it, remove
the entries as above and uninstall it again.

Optional arguments
~~~~~~~~~~~~~~~~~~

On Linux, several file manager can be installed, to create or remove the context
menu shortcut(s) for a specific file manager, use the ``--file_manager`` (``-f``) option:

.. code:: bash

    $ start_jupyter_cm -f nautilus

Help
~~~~

Use the command line help for more information:

.. code:: bash

    $ start_jupyter_cm -h


More information
----------------

Linux
~~~~~

On linux, the context menu shortcuts are created by adding scripts or
configuration files for each file manager. The location of these files are:

- Nautilus: ``~/.local/share/nautilus/scripts``
- Caja: ``~/.config/caja/scripts``
- Dolphin: ``~/.local/share/kservices5/ServiceMenus``
- Nemo: ``~/.local/share/nemo/actions``


Related software
----------------

-  `nbmanager <https://github.com/takluyver/nbmanager>`__ Discover and
   shutdown Jupyter servers.
-  `nbopen <https://github.com/takluyver/nbopen>`__ Open a notebook
   using your filemanager.
