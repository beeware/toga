import os
import platform
import subprocess
import sys
from pathlib import Path

import toga
from toga.constants import COLUMN
from toga.style import Pack

examples_dir = Path(__file__).parents[3]


class ExampleExamplesOverviewApp(toga.App):
    # Button callback functions
    def run(self, widget, **kwargs):
        row = self.table.selection

        env = os.environ.copy()
        env["PYTHONPATH"] = row.path

        subprocess.run([sys.executable, "-m", row.name], env=env)

    def open(self, widget, **kwargs):
        row = self.table.selection

        if platform.system() == "Windows":
            os.startfile(row.path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", row.path])
        else:
            subprocess.run(["xdg-open", row.path])

    def on_example_selected(self, widget, row):
        readme_path = row.path / "README.rst"

        try:
            with open(readme_path) as f:
                readme_text = f.read()
        except OSError:
            readme_text = "README could not be loaded"

        self.info_view.value = readme_text

    def startup(self):
        # ==== Set up main window ======================================================

        self.main_window = toga.MainWindow(title=self.name)

        # Label for user instructions
        label = toga.Label(
            "Please select an example to run",
            style=Pack(padding_bottom=10),
        )

        # ==== Table with examples =====================================================

        self.examples = []

        # search for all folders that contain modules
        for root, dirs, files in os.walk(examples_dir):
            # skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if any(name == "__main__.py" for name in files):
                path = Path(root)
                self.examples.append(dict(name=path.name, path=path.parent))

        self.examples.sort(key=lambda e: e["path"])

        self.table = toga.Table(
            headings=["Name", "Path"],
            data=self.examples,
            on_double_click=self.run,
            on_select=self.on_example_selected,
            style=Pack(padding_bottom=10, flex=1),
        )

        # Buttons
        self.btn_run = toga.Button(
            "Run Example", on_press=self.run, style=Pack(flex=1, padding_right=5)
        )
        self.btn_open = toga.Button(
            "Open folder", on_press=self.open, style=Pack(flex=1, padding_left=5)
        )

        button_box = toga.Box(children=[self.btn_run, self.btn_open])

        # ==== View of example README ==================================================

        self.info_view = toga.MultilineTextInput(
            placeholder="Please select example", readonly=True, style=Pack(padding=1)
        )

        # ==== Assemble layout =========================================================

        left_box = toga.Box(
            children=[self.table, button_box],
            style=Pack(
                direction=COLUMN,
                padding=1,
                flex=1,
            ),
        )

        split_container = toga.SplitContainer(content=[left_box, self.info_view])

        outer_box = toga.Box(
            children=[label, split_container],
            style=Pack(padding=10, direction=COLUMN),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleExamplesOverviewApp(
        "Examples Overview", "org.beeware.widgets.examples_overview"
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
