import asyncio

import toga
from toga.constants import COLUMN, ROW

MAX_PROGRESSBAR_VALUE = 100


class ProgressBarApp(toga.App):
    auto = False

    def startup(self):
        self.main_window = toga.MainWindow(size=(500, 500))

        # set up common styles
        switch_style = {"margin_top": 5}
        label_style = {"flex": 1, "margin_right": 5}
        row_box_style = {"direction": ROW, "margin": 10}
        col_box_style = {"direction": COLUMN, "margin": 10}
        pbar_style = {"width": 150, "margin_right": 5}

        # the user may change the value with +/- buttons
        self.progress_adder = toga.ProgressBar(max=MAX_PROGRESSBAR_VALUE)

        self.minus_button = toga.Button(
            "-",
            on_press=self.decrease_progress,
            flex=1,
        )
        self.plus_button = toga.Button(
            "+",
            on_press=self.increase_progress,
            flex=1,
        )
        self.auto_switch = toga.Switch(
            "Toggle auto mode",
            on_change=self.auto_progress,
            **switch_style,
        )
        self.indeterminate_switch = toga.Switch(
            "Toggle indeterminate mode",
            on_change=self.toggle_indeterminate,
            **switch_style,
        )
        self.running_switch = toga.Switch(
            "Start indeterminate mode",
            on_change=self.toggle_running,
            enabled=False,
            **switch_style,
        )

        # Add the content on the main window
        self.main_window.content = toga.Box(
            **col_box_style,
            children=[
                toga.Box(
                    **col_box_style,
                    children=[
                        toga.Label(
                            "Use the -/+ buttons to change the progress",
                            **label_style,
                        ),
                        self.progress_adder,
                        toga.Box(
                            children=[
                                self.minus_button,
                                self.plus_button,
                            ]
                        ),
                        self.auto_switch,
                        self.indeterminate_switch,
                        self.running_switch,
                    ],
                ),
                toga.Box(
                    **row_box_style,
                    children=[
                        toga.Label("Default", **label_style),
                        toga.ProgressBar(**pbar_style),
                    ],
                ),
                toga.Box(
                    **row_box_style,
                    children=[
                        toga.Label("Running determinate", **label_style),
                        toga.ProgressBar(value=0.5, running=True, **pbar_style),
                    ],
                ),
                toga.Box(
                    **row_box_style,
                    children=[
                        toga.Label("Stopped determinate", **label_style),
                        toga.ProgressBar(value=0.5, running=False, **pbar_style),
                    ],
                ),
                toga.Box(
                    **row_box_style,
                    children=[
                        toga.Label("Running indeterminate", **label_style),
                        toga.ProgressBar(max=None, running=True, **pbar_style),
                    ],
                ),
                toga.Box(
                    **row_box_style,
                    children=[
                        toga.Label("Stopped indeterminate", **label_style),
                        toga.ProgressBar(max=None, running=False, **pbar_style),
                    ],
                ),
            ],
        )

        self.main_window.show()

    async def auto_progress(self, switch, **kw):
        self.minus_button.enabled = not switch.value
        self.plus_button.enabled = not switch.value
        self.indeterminate_switch.enabled = not switch.value
        if switch.value and not self.auto:
            self.auto = True
            if self.progress_adder.is_determinate:
                for i in range(1, 100):
                    self.progress_adder.value = i + 1
                    await asyncio.sleep(0.1)
                    if not switch.value:
                        break
                self.auto = False

    def increase_progress(self, button, **kw):
        if self.progress_adder.is_determinate:
            self.progress_adder.value += 0.1 * self.progress_adder.max

    def decrease_progress(self, button, **kw):
        if self.progress_adder.is_determinate:
            self.progress_adder.value -= 0.1 * self.progress_adder.max

    def toggle_indeterminate(self, switch, **kw):
        self.running_switch.enabled = switch.value
        self.minus_button.enabled = not switch.value
        self.plus_button.enabled = not switch.value
        self.auto_switch.enabled = not switch.value
        if switch.value:
            self.progress_adder.max = None
        else:
            self.progress_adder.max = MAX_PROGRESSBAR_VALUE

    def toggle_running(self, switch, **kw):
        if switch.value:
            switch.text = "Stop indeterminate mode"
            self.progress_adder.start()
        else:
            switch.text = "Start indeterminate mode"
            self.progress_adder.stop()


def main():
    return ProgressBarApp("ProgressBar", "org.beeware.toga.examples.progressbar")


if __name__ == "__main__":
    main().main_loop()
