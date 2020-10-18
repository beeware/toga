from pathlib import Path

import toga
from toga.constants import COLUMN
from toga.style import Pack


class ExampleDocumentApp(toga.DocumentApp):
    def startup(self):
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500),
            resizeable=False, minimizable=False
        )

        self.text_input = toga.MultilineTextInput(style=Pack(flex=1))
        outer_box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Label("Hello!"),
                self.text_input
            ]
        )

        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def load_file(app, file_path):
    with open(file_path, mode="r") as file_object:
        app.text_input.value = file_object.read()


def main():
    # Application class
    #   App name and namespace
    app = ExampleDocumentApp(
        'DocumentApp',
        'org.beeware.widgets.document_app',
        load_document=load_file,
        initial_directory=str(Path(__file__).parent.parent / "resources"),
        document_types=["txt"]
    )
    return app
