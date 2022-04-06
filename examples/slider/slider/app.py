import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

MIN_VAL = -5
MAX_VAL = 15


class SliderApp(toga.App):
    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(1000, 500))

        # set up common styls
        label_style = Pack(flex=1, padding_right=24)
        box_style = Pack(direction=ROW, padding=10)
        slider_style = Pack(flex=1)

        self.discrete_slider_value_label = toga.Label(
            'Slide me or use "ctrl" + "+/-"',
            style=label_style
        )
        self.continuous_slider_value_label = toga.Label(
            "Default Slider is a continuous range between 0 to 1",
            style=label_style
        )

        # Add the content on the main window
        self.discrete_slider = toga.Slider(
            on_change=self.my_discrete_on_change,
            range=(MIN_VAL, MAX_VAL),
            tick_count=MAX_VAL - MIN_VAL + 1,
            style=slider_style
        )
        self.scared_label = toga.Label("Try to catch me!", style=label_style)
        self.main_window.content = toga.Box(
            children=[

                toga.Box(style=box_style, children=[
                    self.continuous_slider_value_label,
                    toga.Slider(
                        on_change=self.my_continuous_on_change,
                        style=slider_style
                    ),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label(
                        "On a scale of 1 to 10, how easy is building a Toga GUI?",
                        style=label_style
                    ),

                    toga.Slider(
                        range=(1, 10),
                        default=10,
                        style=Pack(width=150),
                        tick_count=10
                    ),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("Sliders can be disabled", style=label_style),

                    toga.Slider(enabled=False, style=slider_style),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("Give a Slider some style!", style=label_style),

                    toga.Slider(style=slider_style)
                ]),

                toga.Box(style=box_style, children=[
                    self.discrete_slider_value_label,
                    self.discrete_slider,
                ]),

                toga.Box(style=box_style, children=[
                    self.scared_label,
                    toga.Slider(
                        on_press=self.scared_on_press,
                        on_release=self.scared_on_release,
                        style=slider_style
                    ),
                ]),
            ],
            style=Pack(direction=COLUMN, padding=24)
        )

        self.commands.add(
            toga.Command(
                self.increase_discrete_slider,
                "Increase slider",
                shortcut=toga.Key.MOD_1 + toga.Key.PLUS,
                group=toga.Group.COMMANDS
            ),
            toga.Command(
                self.decrease_discrete_slider,
                "Decrease slider",
                shortcut=toga.Key.MOD_1 + toga.Key.MINUS,
                group=toga.Group.COMMANDS
            )
        )

        self.main_window.show()

    def my_continuous_on_change(self, slider):
        # get the current value of the slider with `slider.value`
        self.continuous_slider_value_label.text = "The slider value changed to {0}".format(
            slider.value
        )

    def my_discrete_on_change(self, slider):
        # get the current value of the slider with `slider.value`
        self.discrete_slider_value_label.text = "The slider value changed to {0}".format(
            slider.value
        )

    def scared_on_press(self, slider):
        self.scared_label.text = "Oh no! they got me!"

    def scared_on_release(self, slider):
        self.scared_label.text = "I am free! Changed to {0}".format(slider.value)

    def increase_discrete_slider(self, widget):
        if self.discrete_slider.tick_value != self.discrete_slider.tick_count:
            self.discrete_slider.tick_value += 1

    def decrease_discrete_slider(self, widget):
        if self.discrete_slider.tick_value != 1:
            self.discrete_slider.tick_value -= 1


def main():
    # App name and namespace
    return SliderApp('Slider', 'org.beeware.examples.slider')
