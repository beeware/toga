import toga


class ExampleDocument(toga.Document):
    def __init__(self, path, app):
        super().__init__(path=path, document_type="Example Document", app=app)

    async def can_close(self):
        return await self.main_window.question_dialog(
            "Are you sure?",
            "Do you want to close this document?",
        )

    def create(self):
        # Create the main window for the document.
        self.main_window = toga.DocumentMainWindow(
            doc=self,
            title=f"Example: {self.path.name}",
        )
        self.main_window.content = toga.MultilineTextInput()

    def read(self):
        with self.path.open() as f:
            self.content = f.read()

        self.main_window.content.value = self.content


def main():
    return toga.DocumentApp(
        "Document App",
        "org.beeware.widgets.documentapp",
        document_types={
            "exampledoc": ExampleDocument,
        },
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
