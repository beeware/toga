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

        self.sliderValueLabel = toga.Label("slide me", style=label_style)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[

                toga.Box(style=box_style, children=[
                    toga.Label(
                        "Default Slider is a continuous range between 0 to 1",
                        style=label_style
                    ),
                    toga.Slider(style=slider_style),
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
                    self.sliderValueLabel,
                    toga.Slider(
                        on_slide=self.my_on_slide,
                        range=(MIN_VAL, MAX_VAL),
                        tick_count=MAX_VAL - MIN_VAL + 1, style=slider_style
                    ),
                ]),
            ],
            style=Pack(direction=COLUMN, padding=24)
        )

        self.main_window.show()

    def my_on_slide(self, slider):
        # get the current value of the slider with `slider.value`
        self.sliderValueLabel.text = "The slider value changed to {0}".format(slider.value)


def main():
    # App name and namespace
    return SliderApp('Slider', 'org.beeware.examples.slider')
