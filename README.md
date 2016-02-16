# start_jupyter_cm

## Description

Add entries to start the Jypyter Notebook and QtConsole from the file manager
context menu. This offers a convenient way of starting Jupyter in a folder.
Currently it only supports Microsoft Windows and GNOME (and its many
derivatives). Contributions to support other OSs/desktop environments are highly
welcome.

### Microsoft Windows
![Jupyter context menu entries in windows](/images/jupyter_cm_windows.png)

In addition to starting the QtConsole or the Jupyter Notebook server and
launching the default browser, in Microsoft Windows the process runs from a
terminal. Closing the terminal closes the QtConsole or the Jupyter server.

### GNOME

![Jupyter context menu entries in windows](/images/jupyter_cm_gnome.png)

Note that in GNOME the processes run in the background. As of Jupyter Notebook
4.1 there is no way to shutdown the server from the notebook UI. To stop
the server one has to manually kill the process. Alternatively, [nbmanager](https://github.com/takluyver/nbmanager) can discover all running
servers and shut them down using via an UI.

## Install

### Microsoft Windows

In Microsoft Windows the preferred way to install this package is by using the
Windows MSI installers provided. Installing the package adds the context menu
entries *for all users** and uninstalling it removes them, so there is nothing
else to do.

### Any platform

Install from pypi using pip e.g.:

```bash
$ pip install start_jupyter_cm
```

After installation, enable the context menu entries from a Python session as
follows:

```python
>>> import start_jupyter_cm
>>> start_jupyter_cm.add_jupyter_here()
```

To remove the context menu entries execute the following in a Python session:

```python
>>> import start_jupyter_cm
>>> start_jupyter_cm.remove_jupyter_here()
```

To uninstall the package:


```bash

$ pip uninstall start_jupyter_cm

```

Note that adding and removing the entries as above may require administration
rights in Microsoft Windows. In Microsoft Windows the entries are added for
all users. In GNOME only for the current user.

Also, be aware that, when not installing from a Microsoft Windows MSI installer,
uninstalling the package does not remove the context menu entries. If you are
left with the context menu entries after uninstalling `start_jupyter_cm`,
reinstall it, remove the entries as above and uninstall it.

## Creating the Windows installers from source

Unfortunatelly, due to [this Python bug](http://bugs.python.org/issue13276),
distutils must be patched to create the Windows MSI binaries.
The MSI installers that we distribute has been created with this patch applied.

## Related software

* [nbmanager](https://github.com/takluyver/nbmanager) Discover and shutdown
  Jupyter servers.
* [nbopen](https://github.com/takluyver/nbopen) Open a notebook using your
  filemanager.

 
