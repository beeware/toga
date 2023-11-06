import asyncio

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

MAX_PROGRESSBAR_VALUE = 100


class ProgressBarApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(500, 500))

        # the user may change the value with +/- buttons
        self.progress_adder = toga.ProgressBar(max=MAX_PROGRESSBAR_VALUE)

        # set up common styles
        label_style = Pack(flex=1, padding_right=5)
        row_box_style = Pack(direction=ROW, padding=10)
        col_box_style = Pack(direction=COLUMN, padding=10)
        pbar_style = Pack(width=150, padding_right=5)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            style=col_box_style,
            children=[
                toga.Box(
                    style=col_box_style,
                    children=[
                        toga.Label(
                            "Use the +/- buttons to change the progress",
                            style=label_style,
                        ),
                        self.progress_adder,
                        toga.Box(
                            children=[
                                toga.Button(
                                    "+",
                                    on_press=self.increase_progress,
                                    style=Pack(flex=1),
                                ),
                                toga.Button(
                                    "-",
                                    on_press=self.decrease_progress,
                                    style=Pack(flex=1),
                                ),
                                toga.Button(
                                    "auto",
                                    on_press=self.auto_progress,
                                    style=Pack(flex=1),
                                ),
                            ]
                        ),
                        toga.Switch(
                            "Toggle indeterminate mode",
                            on_change=self.toggle_indeterminate,
                        ),
                        toga.Switch(
                            "Toggle running mode", on_change=self.toggle_running
                        ),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("Default", style=label_style),
                        toga.ProgressBar(style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("Running determinate", style=label_style),
                        toga.ProgressBar(value=0.5, running=True, style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("Stopped determinate", style=label_style),
                        toga.ProgressBar(value=0.5, running=False, style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("Running indeterminate", style=label_style),
                        toga.ProgressBar(max=None, running=True, style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("Stopped indeterminate", style=label_style),
                        toga.ProgressBar(max=None, running=False, style=pbar_style),
                    ],
                ),
            ],
        )

        self.main_window.show()

    async def auto_progress(self, button, **kw):
        if self.progress_adder.is_determinate:
            for i in range(1, 100):
                self.progress_adder.value = i + 1
                await asyncio.sleep(0.1)

    def increase_progress(self, button, **kw):
        if self.progress_adder.is_determinate:
            self.progress_adder.value += 0.1 * self.progress_adder.max

    def decrease_progress(self, button, **kw):
        if self.progress_adder.is_determinate:
            self.progress_adder.value -= 0.1 * self.progress_adder.max

    def toggle_indeterminate(self, switch, **kw):
        if switch.value:
            self.progress_adder.max = None
        else:
            self.progress_adder.max = MAX_PROGRESSBAR_VALUE

    def toggle_running(self, switch, **kw):
        if switch.value:
            self.progress_adder.start()
        else:
            self.progress_adder.stop()


def main():
    # App name and namespace
    return ProgressBarApp("ProgressBar", "org.beeware.examples.progressbar")


if __name__ == "__main__":
    app = main()
    app.main_loop()
