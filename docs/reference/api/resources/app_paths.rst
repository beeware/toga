App Paths
=========

A mechanism for obtaining platform-appropriate file system locations for an
application.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(App Paths|Component)$)'}

Usage
-----

When Python code executes from the command line, the working directory is a
known location - the location where the application was started. However, when
executing GUI apps, the working directory varies between platforms. As a result,
when specifying file paths, relative paths cannot be used, as there is no
location to which they can be considered relative.

Complicating matters further, operating systems have conventions (and in some
cases, hard restrictions) over where certain file types should be stored. For
example, macOS provides the ``~/Library/Application Support`` folder; Linux
encourages use of the ``~/.config`` folder (amongst others), and Windows
provides the ``AppData/Local`` folder in the user's home directory. Application
sandbox and security policies will prevent sometimes prevent reading or
writing files in any location other than these pre-approved locations.

To assist with finding an appropriate location to store application files, every
Toga application instance has a :attr:`~toga.App.paths` attribute that
returns an instance of :class:`~toga.paths.Paths`. This object provides known
file system locations that are appropriate for storing files of given types,
such as configuration files, log files, cache files, or user data.

Each location provided by the :class:`~toga.paths.Paths` object is a
:class:`pathlib.Path` that can be used to construct a full file path. If
required, additional sub-folders can be created under these locations.

You should not assume that any of these paths already exist. The location is
guaranteed to follow operating system conventions, but the application is
responsible for ensuring the folder exists prior to writing files in these
locations.

Reference
---------

.. autoclass:: toga.paths.Paths
