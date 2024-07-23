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
saved. It also tracks whether the document has been modified. In this example, the code
declares an "Example Document" document type, whose main window contains a
:class:`~toga.MultilineTextInput`. Whenever the content of that widget changes, the
document is marked as modified:

.. code-block:: python

    import toga

    class ExampleDocument(toga.Document):
        document_type = "Example Document"

        def create(self):
            # Create the main window for the document. The window has a single widget;
            # when that widget changes, the document is modified.
            self.main_window = toga.DocumentMainWindow(
                doc=self,
                content=toga.MultilineTextInput(on_change=self.touch),
            )

        def read(self):
            # Read the content of the file represented by the document, and populate the
            # widgets in the main window with that content.
            with self.path.open() as f:
                self.main_window.content.value = f.read()

        def write(self):
            # Save the content currently displayed by the main window.
            with self.path.open("w") as f:
                f.write(self.main_window.content.value)

The document window uses the modification status to determine whether the window is
allowed to close. If a document is modified, the user will be asked if they want to
save changes to the document.

Registering document types
~~~~~~~~~~~~~~~~~~~~~~~~~~

A document type is used by registering it with an app instance. The constructor for
:any:`toga.App` allows you to declare the collection of document types that your app
supports; the first declared document type is treated as the default document type for
your app.

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

By declaring these document types, the app will automatically have file management
commands (New, Open, Save, etc) added.

Reference
---------

.. autoclass:: toga.Document
   :members:
   :undoc-members:
