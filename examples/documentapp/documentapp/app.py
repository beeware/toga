import toga


class ExampleDocument(toga.Document):
    document_type = "Example Document"
    default_extension = ".exampledoc"

    async def can_close(self):
        return await self.main_window.question_dialog(
            "Are you sure?",
            "Do you want to close this document?",
        )

    def create(self):
        # Create the main window for the document.
        self.main_window = toga.DocumentMainWindow(doc=self)
        self.main_window.content = toga.MultilineTextInput()

    def read(self):
        with self.path.open() as f:
            self.main_window.content.value = f.read()

    def write(self):
        with self.path.open("w") as f:
            f.write(self.main_window.content.value)


class ExampleDocumentApp(toga.App):
    def startup(self):
        # A document app has no main window. A window (or windows) will be created from
        # the document(s) specified at the command line; or if no document is specified,
        # the platform will determine how to create an empty document.
        self.main_window = None


def main():
    return ExampleDocumentApp(
        "Document App",
        "org.beeware.toga.examples.documentapp",
        document_types={
            "exampledoc": ExampleDocument,
        },
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
