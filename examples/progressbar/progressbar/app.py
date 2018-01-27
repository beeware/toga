import toga
from colosseum import CSS


class ProgressBarApp(toga.App):

    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(500, 500))
        self.main_window.app = self

        self.progress_demo = toga.ProgressBar()

        # set up common styls
        label_style = CSS(flex=1, padding_right=24)
        box_style = CSS(flex_direction="row", padding=24)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[

                toga.Box(style=CSS(padding=24), children=[
                    toga.Label("Use the +/- buttons to change the progress",
                               style=label_style),

                    self.progress_demo,

                    toga.Box(
                        children=[
                            toga.Button("+", on_press=self.increase_progress,
                                        style=CSS(margin=8, flex=1)),
                            toga.Button("-", on_press=self.decrease_progress,
                                        style=CSS(margin=8, flex=1)),
                        ],
                        style=CSS(flex=1, flex_direction="row")
                    ),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("default ProgressBar", style=label_style),

                    toga.ProgressBar(),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("disabled ProgressBar", style=label_style),

                    toga.ProgressBar(max=None,  running=False),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("indeterminate ProgressBar", style=label_style),

                    toga.ProgressBar(max=None,  running=True),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("inactive determinate ProgressBar", style=label_style),

                    toga.ProgressBar(max=1, running=False, value=0.5),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("working determinate ProgressBar", style=label_style),

                    toga.ProgressBar(max=1, running=True, value=0.5),
                ]),
            ],
            style=CSS(padding=24)
        )

        self.main_window.show()

    def increase_progress(self, button, **kw):
        self.progress_demo.value += 0.1 * self.progress_demo.max

    def decrease_progress(self, button, **kw):
        self.progress_demo.value -= 0.1 * self.progress_demo.max


def main():
    # App name and namespace
    return ProgressBarApp('ProgressBar', 'org.pybee.examples.progressbar')
