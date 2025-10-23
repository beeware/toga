{{ component_header("Document") }}

## Usage

A common requirement for apps is to view or edit a particular type of file. In Toga, you define a [`toga.Document`][] class to represent each type of content that your app is able to manipulate. This [`Document`][toga.Document] class is then registered with your app when the [`App`][toga.App] instance is created.

The [`toga.Document`][] class describes how your document can be read, displayed, and saved. It also tracks whether the document has been modified. In this example, the code declares an "Example Document" document type, which will create files with the extensions `.mydoc` and `.mydocument`; because it is listed first, the `.mydoc` extension will be the default for documents of this type. The main window for this document type contains a [`MultilineTextInput`][toga.MultilineTextInput]. Whenever the content of that widget changes, the document is marked as modified:

```python
import toga

class ExampleDocument(toga.Document):
    description = "Example Document"
    extensions = [`"mydoc", "mydocument"]

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
```

The document window uses the modification status to determine whether the window is allowed to close. If a document is modified, the user will be asked if they want to save changes to the document.

### Registering document types

A document type is used by registering it with an app instance. The constructor for [`toga.App`][] allows you to declare the collection of document types that your app supports. The first declared document type is treated as the default document type for your app; this is the type that will be connected to the keyboard shortcut of the [`NEW`][toga.Command.NEW] command.

After [`startup()`][toga.App.startup] returns, any filenames which were passed to the app by the operating system will be opened using the registered document types. If after this the app still has no windows, then:

- On Windows and GTK, an untitled document of the default type will be opened.
- On macOS, an Open dialog will be shown.

In the following example, the app will be able to manage documents of type `ExampleDocument` or `OtherDocument`, with `ExampleDocument` being the default content type. The app is configured [to not have a single "main" window][assigning-main-window], so the life cycle of the app is not tied to a specific window.

```python
import toga

class ExampleApp(toga.App):
    def startup(self):
        # The app does not have a single main window
        self.main_window = None

app = ExampleApp(
    "Document App",
    "com.example.documentapp",
    document_types=[ExampleDocument, OtherDocument]
)

app.main_loop()
```

By declaring these document types, the app will automatically have file management commands (New, Open, Save, etc) added.

## Reference

::: toga.Document

::: toga.documents.DocumentSet
