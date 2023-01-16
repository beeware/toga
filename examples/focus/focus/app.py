import random

from travertino.constants import COLUMN

import toga
from toga.style import Pack

WIDGETS_GROUP = toga.Group("Widgets", order=2)
FOCUS_ORDER_GROUP = toga.Group("Focus Order", order=3)


class ExampleFocusApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500), resizeable=False, minimizable=False
        )

        self.a_button = toga.Button("A", on_press=self.on_button_press)
        self.b_button = toga.Button("B", on_press=self.on_button_press)
        self.c_button = toga.Button("C", on_press=self.on_button_press)
        self.text_input_focus_count = 0
        self.text_input = toga.TextInput(
            placeholder="I get focused on startup.",
            style=Pack(height=25, width=200, font_size=10),
            on_gain_focus=self.on_textinput_gain_focus,
            on_lose_focus=self.on_textinput_lose_focus,
        )
        self.other_text_input = toga.TextInput(
            placeholder="A non-focussed text input.",
            style=Pack(height=25, width=200, font_size=10),
        )
        self.switch = toga.Switch("Switch", on_change=self.on_switch_toggle)
        self.info_label = toga.Label(
            "Use keyboard shortcuts to focus on the different widgets",
            style=Pack(font_size=10),
        )
        # Add the content on the main window
        self.main_window.content = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(children=[self.a_button, self.b_button, self.c_button]),
                toga.Box(children=[self.text_input]),
                toga.Box(children=[self.other_text_input]),
                toga.Box(children=[self.switch]),
                toga.Box(children=[self.info_label]),
            ],
        )

        self.commands.add(
            toga.Command(
                lambda widget: self.focus_with_label(self.a_button),
                text="Focus on A",
                shortcut=toga.Key.MOD_1 + "a",
                group=WIDGETS_GROUP,
            ),
            toga.Command(
                lambda widget: self.focus_with_label(self.b_button),
                text="Focus on B",
                shortcut=toga.Key.MOD_1 + "b",
                group=WIDGETS_GROUP,
            ),
            toga.Command(
                lambda widget: self.focus_with_label(self.c_button),
                text="Focus on C",
                shortcut=toga.Key.MOD_1 + "c",
                group=WIDGETS_GROUP,
            ),
            toga.Command(
                lambda widget: self.text_input.focus(),
                text="Focus on text input",
                shortcut=toga.Key.MOD_1 + "t",
                group=WIDGETS_GROUP,
            ),
            toga.Command(
                lambda widget: self.focus_with_label(self.switch),
                text="Focus on switch",
                shortcut=toga.Key.MOD_1 + "s",
                group=WIDGETS_GROUP,
            ),
            toga.Command(
                lambda widget: self.order_focus_by_appearance(),
                text="Order focus by appearance",
                shortcut=toga.Key.MOD_1 + "o",
                group=FOCUS_ORDER_GROUP,
            ),
            toga.Command(
                lambda widget: self.order_focus_by_reversed_appearance(),
                text="Order focus by reversed appearance",
                shortcut=toga.Key.MOD_1 + "r",
                group=FOCUS_ORDER_GROUP,
            ),
            toga.Command(
                lambda widget: self.shuffle_focus(),
                text="Shuffle focus order",
                shortcut=toga.Key.MOD_1 + "f",
                group=FOCUS_ORDER_GROUP,
            ),
        )
        # Show the main window
        self.main_window.show()

        self.text_input.focus()

    def on_button_press(self, widget: toga.Button):
        self.info_label.text = "{widget_text} was pressed!".format(
            widget_text=widget.text
        )

    def on_switch_toggle(self, widget: toga.Switch):
        on_off = "on" if widget.value else "off"
        self.info_label.text = f"Switch turned {on_off}!"

    def on_textinput_gain_focus(self, widget: toga.TextInput):
        self.info_label.text = "TextInput has previously had focus " "{} times".format(
            self.text_input_focus_count
        )

    def on_textinput_lose_focus(self, widget: toga.TextInput):
        self.text_input_focus_count += 1

    def focus_with_label(self, widget: toga.Widget):
        widget.focus()
        self.info_label.text = f"{widget.text} is focused!"

    def order_focus_by_appearance(self):
        self.set_focus_order(list(range(1, 7)))

    def order_focus_by_reversed_appearance(self):
        self.set_focus_order(list(range(6, 0, -1)))

    def shuffle_focus(self):
        indices = list(range(1, 7))
        random.shuffle(indices)
        self.set_focus_order(indices)

    def set_focus_order(self, indices):
        assert len(indices) == 6
        self.a_button.tab_index = indices[0]
        self.b_button.tab_index = indices[1]
        self.c_button.tab_index = indices[2]
        self.text_input.tab_index = indices[3]
        self.other_text_input.tab_index = indices[4]
        self.switch.tab_index = indices[5]


def main():
    # Application class
    #   App name and namespace
    app = ExampleFocusApp("Focus", "org.beeware.widgets.focus")
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
