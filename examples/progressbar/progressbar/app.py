import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack
import asyncio

MAX_PROGRESSBAR_VALUE = 100


class ProgressBarApp(toga.App):
    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(500, 500))

        # the user may change the value with +/- buttons
        self.progress_adder = toga.ProgressBar(max=MAX_PROGRESSBAR_VALUE)

        # set up common styles
        label_style = Pack(flex=1, padding_right=5)
        row_box_style = Pack(direction=ROW, padding=10)
        col_box_style = Pack(direction=COLUMN, padding=10)
        pbar_style = Pack(width=100, height=20, padding_right=5)

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
                        toga.Label("default ProgressBar", style=label_style),
                        toga.ProgressBar(style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("disabled ProgressBar", style=label_style),
                        toga.ProgressBar(max=None, running=False, style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("indeterminate ProgressBar", style=label_style),
                        toga.ProgressBar(max=None, running=True, style=pbar_style),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label("determinate ProgressBar", style=label_style),
                        toga.ProgressBar(
                            max=MAX_PROGRESSBAR_VALUE,
                            running=False,
                            value=0.5 * MAX_PROGRESSBAR_VALUE,
                            style=pbar_style,
                        ),
                    ],
                ),
                toga.Box(
                    style=row_box_style,
                    children=[
                        toga.Label(
                            "running determinate ProgressBar", style=label_style
                        ),
                        toga.ProgressBar(
                            max=MAX_PROGRESSBAR_VALUE,
                            running=True,
                            value=0.5 * MAX_PROGRESSBAR_VALUE,
                            style=pbar_style,
                        ),
                    ],
                ),
            ],
        )

        print("is determinate: " + str(self.progress_adder.is_determinate))
        print("is running: " + str(self.progress_adder.is_running))
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
        print("is determinate: " + str(self.progress_adder.is_determinate))

    def toggle_running(self, switch, **kw):
        if switch.value:
            self.progress_adder.start()
        else:
            self.progress_adder.stop()
        print("is running: " + str(self.progress_adder.is_running))


def main():
    # App name and namespace
    return ProgressBarApp("ProgressBar", "org.beeware.examples.progressbar")


if __name__ == '__main__':
    app = main()
    app.main_loop()
