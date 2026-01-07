import toga


class ExampleDocument(toga.Document):
    description = "Example Document"
    extensions = ["exampledoc"]

    def create(self):
        # Create the main window for the document. The window has a single widget;
        # when that widget changes, the document is modified.
        self.main_window = toga.DocumentWindow(
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


class DocumentApp(toga.App):
    def startup(self):
        # A document-based app does not have a single main window. A window (or windows)
        # will be created from the document(s) specified at the command line; or if no
        # document is specified, the platform will determine how to create an initial
        # document.
        self.main_window = None


def main():
    return DocumentApp(
        "Document App",
        "org.beeware.toga.examples.documentapp",
        document_types=[ExampleDocument],
    )


if __name__ == "__main__":
    main().main_loop()
