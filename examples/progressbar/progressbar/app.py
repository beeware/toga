import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

MAX_PROGRESSBAR_VALUE = 100


class ProgressBarApp(toga.App):

    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(500, 500))

        # the user may change the value with +/- buttons
        self.progress_adder = toga.ProgressBar(max=MAX_PROGRESSBAR_VALUE)

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

                toga.Switch("Toggle running mode", on_toggle=self.toggle_running)
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
                toga.Label("determinate ProgressBar", style=label_style),
                toga.ProgressBar(
                    max=MAX_PROGRESSBAR_VALUE,
                    running=False,
                    value=0.5 * MAX_PROGRESSBAR_VALUE),
            ]),

            toga.Box(style=row_box_style, children=[
                toga.Label("running determinate ProgressBar", style=label_style),
                toga.ProgressBar(
                    max=MAX_PROGRESSBAR_VALUE,
                    running=True,
                    value=0.5 * MAX_PROGRESSBAR_VALUE),
            ]),
        ])

        self.main_window.show()

    def increase_progress(self, button, **kw):
        if not self.progress_adder.is_running:
            self.progress_adder.value += 0.1 * self.progress_adder.max

    def decrease_progress(self, button, **kw):
        if not self.progress_adder.is_running:
            self.progress_adder.value -= 0.1 * self.progress_adder.max

    def toggle_running(self, switch, **kw):
        if switch.is_on:
            self.progress_adder.max = None
            self.progress_adder.start()
        else:
            self.progress_adder.max = MAX_PROGRESSBAR_VALUE
            self.progress_adder.stop()


def main():
    # App name and namespace
    return ProgressBarApp('ProgressBar', 'org.beeware.examples.progressbar')
