DocumentMainWindow
==================

A window that can be used as the main interface to a document-based app.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/mainwindow-cocoa.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/mainwindow-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows

    .. figure:: /reference/images/mainwindow-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android |no|

    Not supported

  .. group-tab:: iOS |no|

    Not supported

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

A DocumentMainWindow is the same as a :any:`toga.MainWindow`, except that it is bound to
a :any:`toga.Document` instance, exposed as the :any:`toga.DocumentMainWindow.doc`
attribute.

Instances of :any:`toga.DocumentMainWindow` should be created as part of the
:meth:`~toga.Document.create()` method of an implementation of :any:`toga.Document`.

Reference
---------

.. autoclass:: toga.DocumentMainWindow
