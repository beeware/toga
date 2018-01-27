import toga
from toga.style import Pack
from toga.constants import ROW, COLUMN


class ProgressBarApp(toga.App):

    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(500, 500))

        # the user may change the value with +/- buttons
        self.progress_adder = toga.ProgressBar()

        # the user may switch between "running" mode and a set value
        self.progress_runner = toga.ProgressBar(value=3)

        # set up common styles
        label_style = Pack(flex=1, padding_right=24)
        row_box_style = Pack(direction=ROW, padding=24)
        col_box_style = Pack(direction=COLUMN, padding=24)

        # Add the content on the main window
        self.main_window.content = toga.Box(style=col_box_style, children=[
            toga.Box(style=col_box_style, children=[
                toga.Label("Use the +/- buttons to change the progress",
                           style=label_style),

                self.progress_adder,

                toga.Box(children=[
                    toga.Button("+", on_press=self.increase_progress,
                                style=Pack(flex=1)),
                    toga.Button("-", on_press=self.decrease_progress,
                                style=Pack(flex=1)),
                ]),
            ]),

            toga.Box(style=col_box_style, children=[
                toga.Label("Toggle the switch and watch the running mode change",
                           style=label_style),

                self.progress_runner,
                # toga.Switch("toggle running mode", on_toggle=self.toggle_running)
            ]),

            toga.Box(style=row_box_style, children=[
                toga.Label("default ProgressBar", style=label_style),
                toga.ProgressBar(),
            ]),

            toga.Box(style=row_box_style, children=[
                toga.Label("disabled ProgressBar", style=label_style),
                toga.ProgressBar(max=None,  running=False),
            ]),

            toga.Box(style=row_box_style, children=[
                toga.Label("indeterminate ProgressBar", style=label_style),
                toga.ProgressBar(max=None,  running=True),
            ]),

            toga.Box(style=row_box_style, children=[
                toga.Label("inactive determinate ProgressBar", style=label_style),
                toga.ProgressBar(max=1, running=False, value=0.5),
            ]),

            toga.Box(style=row_box_style, children=[
                toga.Label("working determinate ProgressBar", style=label_style),
                toga.ProgressBar(max=1, running=True, value=0.5),
            ]),
        ])

        self.main_window.show()

    def increase_progress(self, button, **kw):
        self.progress_adder.value += 0.1 * self.progress_adder.max

    def decrease_progress(self, button, **kw):
        self.progress_adder.value -= 0.1 * self.progress_adder.max

    def toggle_running(self, switch, **kw):
        self.progress_runner.running = switch.value


def main():
    # App name and namespace
    return ProgressBarApp('ProgressBar', 'org.pybee.examples.progressbar')
