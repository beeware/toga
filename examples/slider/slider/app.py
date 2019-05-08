import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class SliderApp(toga.App):
    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(700, 500))

        # set up common styls
        label_style = Pack(flex=1, padding_right=24)
        box_style = Pack(direction=ROW, padding=10)
        slider_style = Pack(flex=1)

        self.sliderValueLabel = toga.Label("slide me", style=label_style)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[

                toga.Box(style=box_style, children=[
                    toga.Label("default Slider -- range is 0 to 1",
                        style=label_style),

                    toga.Slider(style=slider_style),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("on a scale of 1 to 10, how easy is GUI with Toga?",
                        style=label_style),

                    toga.Slider(range=(1, 10), default=10, style=Pack(width=150)),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("Sliders can be disabled", style=label_style),

                    toga.Slider(enabled=False, style=slider_style),
                ]),

                toga.Box(style=box_style, children=[
                    toga.Label("give a Slider some style!", style=label_style),

                    toga.Slider(style=slider_style)
                ]),

                toga.Box(style=box_style, children=[
                    self.sliderValueLabel,

                    toga.Slider(on_slide=self.my_on_slide, range=(-40, 58), style=slider_style),
                ]),
            ],
            style=Pack(direction=COLUMN, padding=24)
        )

        self.main_window.show()

    def my_on_slide(self, slider):
        # get the current value of the slider with `slider.value`
        self.sliderValueLabel.text = "The slider value changed to {0}".format(int(slider.value))


def main():
    # App name and namespace
    return SliderApp('Slider', 'org.beeware.examples.slider')
