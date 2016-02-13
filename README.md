# start_jupyter_cm

## Description

Add entries to start the Jypyter Notebook and QtConsole from the file manager
context menu. This offers a convenient way of starting Jupyter in a folder. Currently it only supports Microsoft Windows and GNoME. Contributions to support other OSs/desktop environments are highly welcome.

### Windows
![Jupyter context menu entries in windows](/images/jupyter_cm_windows.png)

### Gnome

![Jupyter context menu entries in windows](/images/jupyter_cm_gnome.png)

## Install

### Windows

In Windows the preferred way to install this package is by using the Windows MSI
installers provided. Installing the package adds the context menu entries and
uninstalling it removes them.

### Any platform

Installed from pypi e.g.:

```bash
$ pip install start_jupyter_cm
```

After installation, enable the context menu entries from a Python session as
follows:

```python
>>> import start_jupyter_cm
>>> start_jupyter_cm.install_jupyter_here()
```

To remove the context menu entries execute the following in a Python session:

```python
>>> import start_jupyter_cm
>>> start_jupyter_cm.uninstall_jupyter_here()
```

Note that adding and removing the entries as above may require administration rights in Microsoft Windows.

To uninstall the package:


```bash

$ pip uninstall start_jupyter_cm

```

Note that when not installing from a Windows MSI installer, uninstalling the
package does not remove the context menu entries.

## Creating the Windows installers from source

Unfortunatelly, due to [this Python bug](http://bugs.python.org/issue13276),
distutils must be patched to create the Windows MSI binaries
[as detailed here](https://code.google.com/p/spyderlib/wiki/PatchingDistutils).
The MSI installers that we distribute has been created with this patch applied.
