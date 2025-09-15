import toga
from toga.constants import COLUMN, ROW

MIN_VAL = -2
MAX_VAL = 12


class SliderApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(1000, 500))

        # set up common styles
        label_style = {"flex": 1, "margin_right": 24}
        box_style = {"direction": ROW, "margin": 10}
        slider_style = {"flex": 1}

        self.continuous_label = toga.Label("Continuous", **label_style)
        self.slider = toga.Slider()
        self.continuous_slider = toga.Slider(
            on_change=self.my_continuous_on_change, **slider_style
        )

        self.disabled_label = toga.Label("Disabled", **label_style)
        self.disabled_slider = toga.Slider(enabled=False, **slider_style)

        self.discrete_label = toga.Label("Discrete\n(with commands)", **label_style)
        self.discrete_slider = toga.Slider(
            on_change=self.my_discrete_on_change,
            min=MIN_VAL,
            max=MAX_VAL,
            tick_count=MAX_VAL - MIN_VAL + 1,
            **slider_style,
        )

        self.scared_label = toga.Label("Try to catch me!", **label_style)
        self.scared_slider = toga.Slider(
            min=100,
            max=300.5,
            value=123.4,
            on_press=self.scared_on_press,
            on_release=self.scared_on_release,
            **slider_style,
        )

        self.main_window.content = toga.Box(
            children=[
                toga.Box(
                    **box_style,
                    children=[self.continuous_label, self.continuous_slider],
                ),
                toga.Box(
                    **box_style,
                    children=[self.disabled_label, self.disabled_slider],
                ),
                toga.Box(
                    **box_style,
                    children=[self.discrete_label, self.discrete_slider],
                ),
                toga.Box(
                    **box_style,
                    children=[self.scared_label, self.scared_slider],
                ),
            ],
            direction=COLUMN,
            margin=24,
        )

        self.commands.add(
            toga.Command(
                self.increase_discrete_slider,
                "Increase slider",
                shortcut=toga.Key.MOD_1 + toga.Key.PLUS,
                group=toga.Group.COMMANDS,
            ),
            toga.Command(
                self.decrease_discrete_slider,
                "Decrease slider",
                shortcut=toga.Key.MOD_1 + toga.Key.MINUS,
                group=toga.Group.COMMANDS,
            ),
        )

        self.main_window.show()

    def my_continuous_on_change(self, slider):
        self.continuous_label.text = f"Value = {slider.value:.4f}"
        self.disabled_slider.value = slider.value

    def my_discrete_on_change(self, slider):
        self.discrete_label.text = f"Value = {slider.value}"

    def scared_on_press(self, slider):
        self.scared_label.text = "They got me!"

    def scared_on_release(self, slider):
        self.scared_label.text = f"Value = {slider.value:.4f}"

    def increase_discrete_slider(self, widget):
        if self.discrete_slider.tick_value != self.discrete_slider.tick_count:
            self.discrete_slider.tick_value += 1

    def decrease_discrete_slider(self, widget):
        if self.discrete_slider.tick_value != 1:
            self.discrete_slider.tick_value -= 1


def main():
    return SliderApp("Slider", "org.beeware.toga.examples.slider")


if __name__ == "__main__":
    main().main_loop()
