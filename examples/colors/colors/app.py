import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
from travertino import colors


class ColorsApp(toga.App):
    def change_color_foreground(self, widget):
        if widget.id == "reset":
            color = None
        else:
            color = widget.id

        for widget in self.example_widgets:
            widget.style.color = color

    def change_color_background(self, widget):
        if widget.id == "reset":
            color = None
        else:
            color = widget.id

        for widget in self.example_widgets:
            widget.style.background_color = color

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(650, 800))

        # create widgets to test colors on
        button = toga.Button("This is a button", style=Pack(padding=5))
        label = toga.Label("This is a Label", style=Pack(padding=5))
        multiline_text_input = toga.MultilineTextInput(
            initial="This is a Multiline Text Input field!",
            style=Pack(padding=5, flex=1),
        )
        number_input = toga.NumberInput(default=1337, style=Pack(padding=5))
        password_input = toga.PasswordInput(initial="adminadmin", style=Pack(padding=5))
        progress_bar = toga.ProgressBar(
            max=100, value=50, running=True, style=Pack(padding=5)
        )
        selection = toga.Selection(
            items=["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"],
            style=Pack(padding=5),
        )
        slider = toga.Slider(style=Pack(padding=5))
        switch = toga.Switch("Switch", style=Pack(padding=5))
        table = toga.Table(
            headings=["Heading 1", "Heading 2"],
            data=[
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
                ("value 1", "value 2"),
            ],
            missing_value="none",
            style=Pack(padding=5, flex=1),
        )
        text_input = toga.TextInput(
            initial="This is a Text input field!",
            style=Pack(padding=5),
        )

        scroll_container = toga.ScrollContainer(
            horizontal=True,
            vertical=True,
            style=Pack(direction=COLUMN, flex=1),
        )
        temp_box = toga.Box(
            children=[toga.Label("Scrollcontainer example! filled with labels.")],
            style=Pack(direction=COLUMN),
        )
        for x in range(20):
            temp_box.add(toga.Label("Label"))
        scroll_container.content = temp_box

        box_label = toga.Label("This is a Box:", style=Pack(padding=5))
        box = toga.Box(style=Pack(flex=1, padding=5))

        self.widget_box = toga.Box(
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
            # Use a cyan background so that color changes are obvious
            style=Pack(direction=COLUMN, flex=1, background_color="cyan"),
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
        change_fcolor_r = toga.Button(
            "Red",
            id=colors.RED,
            on_press=self.change_color_foreground,
            style=Pack(padding=5, width=100),
        )
        change_fcolor_g = toga.Button(
            "Green",
            id=colors.GREEN,
            on_press=self.change_color_foreground,
            style=Pack(padding=5, width=100),
        )
        change_fcolor_b = toga.Button(
            "Blue",
            id=colors.BLUE,
            on_press=self.change_color_foreground,
            style=Pack(padding=5, width=100),
        )
        change_fcolor_reset = toga.Button(
            "Reset",
            id="reset",
            on_press=self.change_color_foreground,
            style=Pack(padding=5, width=100),
        )
        change_bcolor_r = toga.Button(
            "Red",
            id=colors.RED,
            on_press=self.change_color_background,
            style=Pack(padding=5, width=100),
        )
        change_bcolor_g = toga.Button(
            "Green",
            id=colors.GREEN,
            on_press=self.change_color_background,
            style=Pack(padding=5, width=100),
        )
        change_bcolor_b = toga.Button(
            "Blue",
            id=colors.BLUE,
            on_press=self.change_color_background,
            style=Pack(padding=5, width=100),
        )
        change_bcolor_t = toga.Button(
            "Transparent",
            id=colors.TRANSPARENT,
            on_press=self.change_color_background,
            style=Pack(padding=5, width=100),
        )
        change_bcolor_reset = toga.Button(
            "Reset",
            id="reset",
            on_press=self.change_color_background,
            style=Pack(padding=5, width=100),
        )

        control_box = toga.Box(
            children=[
                toga.Label("Color selection:"),
                change_fcolor_r,
                change_fcolor_g,
                change_fcolor_b,
                change_fcolor_reset,
                toga.Label("Background color selection:", style=Pack(padding_top=10)),
                change_bcolor_r,
                change_bcolor_g,
                change_bcolor_b,
                change_bcolor_t,
                change_bcolor_reset,
            ],
            style=Pack(direction=COLUMN, padding=5),
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.widget_box, control_box],
            style=Pack(flex=1, direction=ROW, padding=10),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ColorsApp("Colors", "org.beeware.widgets.colors")


if __name__ == "__main__":
    app = main()
    app.main_loop()
