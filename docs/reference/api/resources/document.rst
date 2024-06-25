Document
========

A representation of a file on disk that will be displayed in one or more windows.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :include: {0: '^Document$'}


Usage
-----

A common requirement for apps is to view or edit a particular type of file. In Toga, you
define a :class:`toga.Document` class to represent each type of content that your app is
able to manipulate. This :class:`~toga.Document` class is then registered with your app
when the :class:`~toga.App` instance is created.

The :class:`toga.Document` class describes how your document can be read, displayed, and
saved. In this example, the code declares an "Example Document" document type, whose
main window contains a :class:`~toga.MultilineTextInput`:

.. code-block:: python

    import toga

    class ExampleDocument(toga.Document):
        document_type = "Example Document"

        def create(self):
            # Create the representation for the document's main window
            self.main_window = toga.DocumentMainWindow(
                doc=self,
                content=toga.MultilineTextInput(),
            )

        def read(self):
            # Read the document
            with self.path.open() as f:
                self.main_window.content.value = f.read()

        def write(self):
            # Save the document
            with self.path.open("w") as f:
                f.write(self.main_window.content.value)

This document class can then be registered with an app instance. The constructor for
:any:`toga.App` allows you to declare the full collection of document types that your
app supports; the first declared document type is treated as the default document type
for your app.

In the following example, the ``ExampleDocument`` class is set as the default content
type, and is registered as representing documents with extension ``.mydoc`` or
``.mydocument``. The app will also support documents with the extension ``.otherdoc``.
The app is configured :ref:`to not have a single "main" window <assigning-main-window>`,
so the life cycle of the app is not tied to a specific window. It will use
``ExampleDocument`` (with extension ``mydoc``) as the default document type:

.. code-block:: python

    import toga

    class ExampleApp(toga.App):
        def startup(self):
            # The app does not have a single main window
            self.main_window = None

    app = ExampleApp(
        "Document App",
        "com.example.documentapp",
        document_types={
            "mydoc": ExampleDocument,
            "mydocument": ExampleDocument,
            "otherdoc": OtherDocument,
        }
    )

    app.main_loop()

Reference
---------

.. autoclass:: toga.Document
   :members:
   :undoc-members:
