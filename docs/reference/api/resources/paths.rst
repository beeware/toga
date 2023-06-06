App Paths
==========

A mechanism for obtaining platform-appropriate file system locations for an
application.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(App Paths|Component)$)'}

Usage
-----

When Python code executes from the command line, the working directory is a
known location - the location where the application was started. However, when
building GUI apps, there is no "working directory". As a result, when specifying
file paths, relative paths cannot be used, as there is no location to which they
can be considered relative.

Complicating matters further, operating systems have conventions over where
certain file types should be stored. For example, macOS provides the
``~/Library/Application Support`` folder; Linux encourages use of the
``~/.config`` folder (amongst others), and Windows provides the
``AppData/Local`` folder.

To assist with finding an appropriate location to store application files, every
Toga application has a ``paths`` object that provides known file system
locations that are appropriate for storing files of given types, such as
configuration files, log files, cache files, or user documents.

Each location provided by the ``paths`` object is a :class:`Pathlib.Path` that
can be used to construct a full file path. If required, additional sub-folders
can be created under these locations.

The paths returned are *not* guaranteed to be empty or unique. For example, you
should not assume that the user data location *only* contains user data files.
Depending on platform conventions, there may be other files or folders.

You should not assume that any of these paths already exist. The location is
guaranteed to follow operating system conventions, but the application is
responsible for ensuring the folder exists prior to writing files in these
locations.

Reference
---------

.. autoclass:: toga.paths.Paths
   :members:
   :undoc-members:
