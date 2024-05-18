2.4.0.dev0 (UNRELEASED)
-----------------------

2.3.2 (2024-05-18)
------------------
* Update GitHub workflows
* Add explicit support for python 3.11, 3.12 and 3.13 and drop python 3.7
* Add explicit support for python 3.10 and drop python 3.6
* Pin third party GitHub actions to SHA and update GitHub actions

2.3.1 (2021-09-01)
------------------
The is a patch release:

* Clarify tested version on MacOSX (10.14.6 to 11.5.1).
* Improve setting testing on CI.
* Fix links to images in `README.rst` file following renaming the `master`
  branch to `main`.

2.3.0 (2021-04-11)
------------------
This is a minor release:

* Move CI to GitHub Actions and add releasing guide
* Add support for space in path

2.2.0 (2020-07-02)
------------------
This is a minor release:

* Improve documentation (README.rst).
* Add test suite on Linux and Windows, setup Travis and Appveyor.
* Add support for Nemo file manager (Linux/Cinnamon).
* Add support for Caja file manager (Linux/MATE).
* Add option to select a specific file manager (Linux).
* Remove unnecessary dependencies.
* Add support for Dolphin file manager (Linux/KDE).

2.1.0 (2019-10-09)
------------------
This is a minor release:

* Add support for MacOSX.
* Fix path to python for running scripts on gnome.

2.0.0 (2019-07-28)
------------------
This is a major release changing the API:

* Merge installation and removal command into one single commands
  ``start_jupyter_cm`` that takes a ``--remove`` argument.
* Add test suite and continuous integration in travis and appveyor.

1.4.0 (2019-06-28)
------------------
* Add support for conda environment on linux.
* Create shortcut only when the executable is installed.
* Drop python 2.7 support.
* Update documentation (README.rst) and installation instructions.

1.3.1 (2019-06-27)
------------------
* Tidy up setup scripts to fix conda-forge build on windows

1.3.0 (2019-06-19)
------------------
* Add support for single user installation on windows.
* Add support for conda environment on windows.

1.2.0 (2018-10-24)
------------------
* Add Jupyter lab entry.
* Change deprecated `gvfs-set-attribute` attribute to `gio set` for gnome.

1.1.2 (2016-05-27)
------------------
* Add global variable start_jupyter_cm.windows.WPSCRIPTS_FOLDER to define the WinPython scripts folder.

1.1.0 (2018-02-19)
------------------
* Add support for WinPython
* Open jupyter notebook inside selected folder instead of parent directory.
