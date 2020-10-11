from travertino.constants import COLUMN

import toga
from toga.style import Pack

WIDGETS_GROUP = toga.Group("Widgets", order=2)


class ExampleFocusApp(toga.App):

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500),
            resizeable=False, minimizable=False
        )

        self.a_button = toga.Button(
            "X",
            on_press=self.on_button_press,
            on_focus_gain=self.on_button_focus_gain,
            on_focus_loss=self.on_button_focus_loss,
        )
        self.b_button = toga.Button(
            "Y",
            on_press=self.on_button_press,
            on_focus_gain=self.on_button_focus_gain,
            on_focus_loss=self.on_button_focus_loss,
        )
        self.c_button = toga.Button(
            "Z",
            on_press=self.on_button_press,
            on_focus_gain=self.on_button_focus_gain,
            on_focus_loss=self.on_button_focus_loss,
        )
        self.text_input = toga.TextInput(
            placeholder="I get focused on startup.",
            on_change=self.on_text_input_change,
            on_focus_gain=self.on_text_input_focus_gain,
            style=Pack(height=25, width=200, font_size=10)
        )
        self.switch = toga.Switch(
            "Switch",
            on_toggle=self.on_switch_toggle,
            on_focus_gain=self.on_switch_focus_gain
        )
        self.slider = toga.Slider(
            range=(0, 10),
            tick_count=11,
            on_change=self.on_slider_change,
            on_focus_gain=self.on_slider_focus_gain
        )
        self.info_label = toga.Label(
            "",
            style=Pack(font_size=10),
            on_focus_gain=lambda w: self.set_reset_label()
        )
        # Add the content on the main window
        self.main_window.content = toga.Box(
            style=Pack(direction=COLUMN), children=[
                toga.Box(children=[self.a_button, self.b_button, self.c_button]),
                toga.Box(children=[self.text_input]),
                toga.Box(children=[self.slider]),
                toga.Box(children=[self.switch]),
                toga.Box(children=[self.info_label])
            ]
        )

        self.commands.add(
            toga.Command(
                lambda widget: self.a_button.focus(),
                label="Focus on A",
                shortcut=toga.Key.MOD_1 + "x",
                group=WIDGETS_GROUP,
                order=0,
            ),
            toga.Command(
                lambda widget: self.b_button.focus(),
                label="Focus on B",
                shortcut=toga.Key.MOD_1 + "y",
                group=WIDGETS_GROUP,
                order=1,
            ),
            toga.Command(
                lambda widget: self.c_button.focus(),
                label="Focus on C",
                shortcut=toga.Key.MOD_1 + "z",
                group=WIDGETS_GROUP,
                order=2,
            ),
            toga.Command(
                lambda widget: self.text_input.focus(),
                label="Focus on text input",
                shortcut=toga.Key.MOD_1 + "t",
                group=WIDGETS_GROUP,
                order=3,
            ),
            toga.Command(
                lambda widget: self.slider.focus(),
                label="Focus on Slider",
                shortcut=toga.Key.MOD_1 + "l",
                group=WIDGETS_GROUP,
                order=4,
            ),
            toga.Command(
                lambda widget: self.switch.focus(),
                label="Focus on switch",
                shortcut=toga.Key.MOD_1 + "w",
                group=WIDGETS_GROUP,
                order=5,
            ),
            toga.Command(
                lambda widget: self.info_label.focus(),
                label="Reset focus",
                shortcut=toga.Key.MOD_1 + "r",
                group=WIDGETS_GROUP,
                section=1,
                order=0,
            )
        )
        # Show the main window
        self.main_window.show()

        self.text_input.focus()
        self.set_reset_label()

    def on_button_press(self, widget: toga.Button):
        self.info_label.text = "{widget_label} was pressed!".format(
            widget_label=widget.label
        )

    def on_button_focus_gain(self, widget: toga.Button):
        widget.style.background_color = toga.colors.BLUE
        self.focus_label(widget.label)

    def on_text_input_change(self, widget):
        self.info_label.text = "TextInput has changed!"

    def on_text_input_focus_gain(self, widget: toga.TextInput):
        self.focus_label("TextInput")

    def on_switch_focus_gain(self, widget: toga.Switch):
        self.focus_label(widget.label)

    @classmethod
    def on_button_focus_loss(cls, widget: toga.Button):
        widget.style.background_color = toga.colors.TRANSPARENT

    def on_switch_toggle(self, widget: toga.Switch):
        on_off = "on" if widget.is_on else "off"
        self.info_label.text = "Switch turned {on_off}!".format(on_off=on_off)

    def on_slider_focus_gain(self, widget: toga.Slider):
        self.focus_label("Slider")

    def on_slider_change(self, widget: toga.Slider):
        self.info_label.text = "Slider value change to {}!".format(widget.value)

    def focus_label(self, name: str):
        self.info_label.text = "{name} is focused!".format(name=name)

    def set_reset_label(self):
        self.info_label.text = "Use keyboard shortcuts to focus on the different widgets."


def main():
    # Application class
    #   App name and namespace
    app = ExampleFocusApp('Focus', 'org.beeware.widgets.focus')
    return app
