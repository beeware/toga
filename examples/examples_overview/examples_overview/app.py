import os
import platform
import subprocess
import sys
import webbrowser
from pathlib import Path

import markdown

import toga
from toga.constants import COLUMN

examples_dir = Path(__file__).parents[2]


class ExamplesOverviewApp(toga.App):
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

    def on_example_selected(self, widget):
        readme_path = widget.selection.path / "README.md"

        try:
            with open(readme_path) as f:
                readme_text = f.read()
        except OSError:
            readme_text = "README could not be loaded"

        self.info_view.set_content(None, markdown.markdown(readme_text))

    def no_navigation(self, widget, url, **kwargs):
        webbrowser.open(url)
        return False

    def startup(self):
        # ==== Set up main window ======================================================

        self.main_window = toga.MainWindow()

        # Label for user instructions
        label = toga.Label(
            "Please select an example to run",
            margin_bottom=10,
        )

        # ==== Table with examples =====================================================

        self.examples = []

        # search for all folders that contain modules
        for root, dirs, files in os.walk(examples_dir):
            # skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "build"]
            if any(name == "__main__.py" for name in files):
                path = Path(root)
                self.examples.append({"name": path.name, "path": path.parent})

        self.examples.sort(key=lambda e: e["path"])

        self.table = toga.Table(
            headings=["Name", "Path"],
            data=self.examples,
            on_activate=self.run,
            on_select=self.on_example_selected,
            margin_bottom=10,
            flex=1,
        )

        # Buttons
        self.btn_run = toga.Button(
            "Run Example", on_press=self.run, flex=1, margin_right=5
        )
        self.btn_open = toga.Button(
            "Open folder", on_press=self.open, flex=1, margin_left=5
        )

        button_box = toga.Box(children=[self.btn_run, self.btn_open])

        # ==== View of example README ==================================================

        self.info_view = toga.WebView(
            content="Please select example",
            margin=1,
            on_navigation_starting=self.no_navigation,
        )

        # ==== Assemble layout =========================================================

        left_box = toga.Box(
            children=[self.table, button_box],
            direction=COLUMN,
            margin=1,
            flex=1,
        )

        split_container = toga.SplitContainer(
            content=[left_box, self.info_view],
            flex=1,
        )

        outer_box = toga.Box(
            children=[label, split_container],
            margin=10,
            direction=COLUMN,
            flex=1,
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExamplesOverviewApp(
        "Examples Overview", "org.beeware.toga.examples.examples_overview"
    )


if __name__ == "__main__":
    main().main_loop()
