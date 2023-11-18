DocumentApp
===========

The top-level representation of an application that manages documents.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(DocumentApp|Component))'}


Usage
-----

A DocumentApp is a specialized subclass of App that is used to manage documents. A
DocumentApp does *not* have a main window; each document that the app manages has it's
own main window. Each document may also define additional windows, if necessary.

The types of documents that the DocumentApp can manage must be declared as part of the
instantiation of the DocumentApp. This requires that you define a subclass of
:class:`toga.Document` that describes how your document can be read and displayed. In
this example, the code declares an "Example Document" document type, whose files have an
extension of ``mydoc``:

.. code-block:: python

    import toga

    class ExampleDocument(toga.Document):
        def __init__(self, path, app):
            super().__init__(document_type="Example Document", path=path, app=app)

        def create(self):
            # Create the representation for the document's main window
            self.main_window = toga.DocumentMainWindow(self)
            self.main_window.content = toga.MultilineTextInput()

        def read(self):
            # Put your logic to read the document here. For example:
            with self.path.open() as f:
                self.content = f.read()

            self.main_window.content.value = self.content

    app = toga.DocumentApp("Document App", "com.example.document", {"mydoc": MyDocument})
    app.main_loop()

The exact behavior of a DocumentApp is slightly different on each platform, reflecting
platform differences.

macOS
~~~~~

On macOS, there is only ever a single instance of a DocumentApp running at any given
time. That instance can manage multiple documents. If you use the Finder to open a
second document of a type managed by the DocumentApp, it will be opened in the existing
DocumentApp instance. Closing all documents will not cause the app to exit; the app will
keep executing until explicitly exited.

If the DocumentApp is started without an explicit file reference, a file dialog will be
displayed prompting the user to select a file to open. If this dialog can be dismissed,
the app will continue running. Selecting "Open" from the file menu will also display this
dialog; if a file is selected, a new document window will be opened.

Linux/Windows
~~~~~~~~~~~~~

On Linux and Windows, each DocumentApp instance manages a single document. If your app
is running, and you use the file manager to open a second document, a second instance of
the app will be started. If you close a document's main window, the app instance
associated with that document will exit, but any other app instances will keep running.

If the DocumentApp is started without an explicit file reference, a file dialog will be
displayed prompting the user to select a file to open. If this dialog is dismissed, the
app will continue running, but will show an empty document. Selecting "Open" from the
file menu will also display this dialog; if a file is selected, the current document
will be replaced.

Reference
---------

.. autoclass:: toga.DocumentApp
   :members:
   :undoc-members:

.. autoclass:: toga.Document
   :members:
   :undoc-members:
