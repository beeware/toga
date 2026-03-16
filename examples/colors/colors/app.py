from travertino import colors

import toga
from toga.constants import COLUMN, ROW


class ColorsApp(toga.App):
    def change_color_foreground(self, color):
        def _change_color_foreground(widget):
            for widget in self.example_widgets:
                if color is None:
                    del widget.style.color
                else:
                    widget.style.color = color

        return _change_color_foreground

    def change_color_background(self, color):
        def _change_color_background(widget):
            for widget in self.example_widgets:
                if color is None:
                    del widget.style.background_color
                else:
                    widget.style.background_color = color

        return _change_color_background

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(size=(700, 800))

        # create widgets to test colors on
        button = toga.Button("This is a button")
        label = toga.Label("This is a Label")
        multiline_text_input = toga.MultilineTextInput(
            value="This is a Multiline Text Input field!",
            placeholder="placeholder",
            flex=1,
        )
        number_input = toga.NumberInput(value=1337)
        password_input = toga.PasswordInput(value="adminadmin")
        progress_bar = toga.ProgressBar(max=100, value=50, running=True)
        selection = toga.Selection(
            items=["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"],
        )
        slider = toga.Slider()
        switch = toga.Switch("Switch")
        table = toga.Table(
            columns=["Heading 1", "Heading 2"],
            data=[
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
            ],
            missing_value="none",
            flex=1,
        )
        text_input = toga.TextInput(
            value="This is a Text input field!", placeholder="placeholder"
        )

        scroll_container = toga.ScrollContainer(
            horizontal=True,
            vertical=True,
            direction=COLUMN,
            flex=1,
        )
        temp_box = toga.Box(
            children=[toga.Label("Scrollcontainer example! filled with labels.")],
            direction=COLUMN,
        )
        for x in range(20):
            temp_box.add(toga.Label(f"Label {x}"))
        scroll_container.content = temp_box

        box_label = toga.Label("This is a Box:")
        box = toga.Box(flex=1)

        self.widget_box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        button,
                        label,
                        multiline_text_input,
                        number_input,
                        password_input,
                        progress_bar,
                        selection,
                        slider,
                        switch,
                        table,
                        text_input,
                        scroll_container,
                        box_label,
                        box,
                    ],
                    # Stack widgets vertically, and add margin so the
                    # background cyan of the parent is a border around the
                    # widgets
                    direction=COLUMN,
                    flex=1,
                    margin=10,
                    gap=10,
                )
            ],
            # Use a cyan background so that color changes are obvious
            direction=COLUMN,
            flex=1,
            background_color="cyan",
        )
        # These are the widgets that will have their color changed.
        self.example_widgets = [
            button,
            label,
            multiline_text_input,
            number_input,
            password_input,
            progress_bar,
            selection,
            slider,
            switch,
            table,
            text_input,
            scroll_container,
            box,
        ]

        # setup control box
        button_style = {"margin": 2, "width": 100}
        change_fcolor_r = toga.Button(
            "Red",
            on_press=self.change_color_foreground(colors.RED),
            **button_style,
        )
        change_fcolor_g = toga.Button(
            "Green",
            on_press=self.change_color_foreground(colors.GREEN),
            **button_style,
        )
        change_fcolor_b = toga.Button(
            "Blue",
            on_press=self.change_color_foreground(colors.BLUE),
            **button_style,
        )
        change_fcolor_reset = toga.Button(
            "Reset",
            on_press=self.change_color_foreground(None),
            **button_style,
        )
        change_bcolor_r = toga.Button(
            "Red",
            on_press=self.change_color_background(colors.RED),
            **button_style,
        )
        change_bcolor_g = toga.Button(
            "Green",
            on_press=self.change_color_background(colors.GREEN),
            **button_style,
        )
        change_bcolor_b = toga.Button(
            "Blue",
            on_press=self.change_color_background(colors.BLUE),
            **button_style,
        )
        change_bcolor_t = toga.Button(
            "Transparent",
            on_press=self.change_color_background(colors.TRANSPARENT),
            **button_style,
        )
        change_bcolor_reset = toga.Button(
            "Reset",
            on_press=self.change_color_background(None),
            **button_style,
        )

        control_box = toga.Box(
            children=[
                toga.Label("Foreground"),
                change_fcolor_r,
                change_fcolor_g,
                change_fcolor_b,
                change_fcolor_reset,
                toga.Label("Background", margin_top=10),
                change_bcolor_r,
                change_bcolor_g,
                change_bcolor_b,
                change_bcolor_t,
                change_bcolor_reset,
            ],
            direction=COLUMN,
            margin=5,
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.widget_box, control_box],
            flex=1,
            direction=ROW,
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ColorsApp("Colors", "org.beeware.toga.examples.colors")


if __name__ == "__main__":
    main().main_loop()
