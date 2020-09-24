import sys
import os
import subprocess
import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW, RIGHT


examples_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ExampleExamplesOverviewApp(toga.App):
    # Button callback functions
    def run(self, widget, **kwargs):

        row = self.table.selection

        env = os.environ.copy()
        env["PYTHONPATH"] = row.path

        self._process = subprocess.Popen(
            [sys.executable, '-m', row.name],
            env=env,
        )

    def startup(self):

        self._process = None

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label for user instructions
        self.label = toga.Label(
            'Please select an example and press run',
            style=Pack(padding_bottom=10),
        )

        # Table with example programs
        self.examples = []

        # search for all folders that contain modules
        for root, dirs, files in os.walk(examples_dir):
            # skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if any(name == '__main__.py' for name in files):
                example_path, example_name = os.path.split(root)
                self.examples.append(
                    dict(
                        name=example_name,
                        path=example_path
                    )
                )

        self.examples.sort(key=lambda e: e['path'])

        self.table = toga.Table(
            headings=["Name", "Path"],
            data=self.examples,
            on_double_click=self.run,
            style=Pack(padding_bottom=10, flex=1),
        )

        # Buttons
        self.btn_run = toga.Button('Run Example', on_press=self.run)

        # Outermost box
        outer_box = toga.Box(
            children=[self.label, self.table, self.btn_run],
            style=Pack(
                direction=COLUMN,
                flex=1,
                padding=10,
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleExamplesOverviewApp('Examples Overview', 'org.beeware.widgets.examples_overview')


if __name__ == '__main__':
    app = main()
    app.main_loop()
