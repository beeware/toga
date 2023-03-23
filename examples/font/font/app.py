import toga
from toga.constants import BOLD, COLUMN, ITALIC, MONOSPACE, NORMAL, ROW
from toga.style import Pack


class ExampleFontExampleApp(toga.App):
    textpanel = None

    # Button callback functions
    def do_clear(self, widget, **kwargs):
        self.textpanel.value = ""

    def do_weight(self, widget, **kwargs):
        if widget.style.font_weight == NORMAL:
            widget.style.font_weight = BOLD
        else:
            widget.style.font_weight = NORMAL

    def do_style(self, widget, **kwargs):
        if widget.style.font_style == NORMAL:
            widget.style.font_style = ITALIC
        else:
            widget.style.font_style = NORMAL

    def do_monospace_button(self, widget):
        self.textpanel.value += widget.text + "\n"

    def do_icon_button(self, widget):
        self.textpanel.value += widget.id + "\n"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # register fonts
        toga.Font.register(
            "awesome-free-solid", "resources/Font Awesome 5 Free-Solid-900.otf"
        )
        toga.Font.register("Endor", "resources/ENDOR___.ttf")
        toga.Font.register("Endor", "resources/ENDOR___.ttf", weight=BOLD)
        toga.Font.register("Endor", "resources/ENDOR___.ttf", style=ITALIC)
        toga.Font.register("Endor", "resources/ENDOR___.ttf", weight=BOLD, style=ITALIC)
        toga.Font.register("Roboto", "resources/Roboto-Regular.ttf")
        toga.Font.register("Roboto", "resources/Roboto-Bold.ttf", weight=BOLD)
        toga.Font.register("Roboto", "resources/Roboto-Italic.ttf", style=ITALIC)
        toga.Font.register(
            "Roboto", "resources/Roboto-BoldItalic.ttf", weight=BOLD, style=ITALIC
        )

        # Buttons
        btn_box1 = toga.Box(
            style=Pack(direction=ROW, padding_bottom=10),
            children=[
                toga.Button("Clear", on_press=self.do_clear),
                toga.Button("Weight", on_press=self.do_weight),
                toga.Button("Style", on_press=self.do_style),
            ],
        )

        btn1 = toga.Button(
            "Monospace",
            on_press=self.do_monospace_button,
            style=Pack(font_family=MONOSPACE),
        )
        btn2 = toga.Button(
            "\uf0c5",
            id="copy",
            on_press=self.do_icon_button,
            style=Pack(font_family="awesome-free-solid", font_size=14, width=50),
        )
        btn3 = toga.Button(
            "\uf0ea",
            id="paste",
            on_press=self.do_icon_button,
            style=Pack(font_family="awesome-free-solid", font_size=14, width=50),
        )
        btn4 = toga.Button(
            "\uf0a9",
            id="arrow-right",
            on_press=self.do_icon_button,
            style=Pack(font_family="awesome-free-solid", font_size=14, width=50),
        )
        btn_box2 = toga.Box(
            style=Pack(direction=ROW, padding_bottom=10),
            children=[btn1, btn2, btn3, btn4],
        )

        # Labels
        lbl1 = toga.Label("Endor", style=Pack(font_family="Endor", font_size=14))
        lbl2 = toga.Label(
            "Endor bold",
            style=Pack(font_family="Endor", font_size=14, font_weight=BOLD),
        )
        lbl3 = toga.Label(
            "Endor italic",
            style=Pack(font_family="Endor", font_size=14, font_style=ITALIC),
        )
        lbl4 = toga.Label(
            "Endor bold italic",
            style=Pack(
                font_family="Endor",
                font_size=14,
                font_weight=BOLD,
                font_style=ITALIC,
            ),
        )
        lbl5 = toga.Label(
            "Roboto",
            style=Pack(font_family="Roboto", font_size=14),
        )
        lbl6 = toga.Label(
            "Roboto bold",
            style=Pack(font_family="Roboto", font_size=14, font_weight=BOLD),
        )
        lbl7 = toga.Label(
            "Roboto italic",
            style=Pack(font_family="Roboto", font_size=14, font_style=ITALIC),
        )
        lbl8 = toga.Label(
            "Roboto bold italic",
            style=Pack(
                font_family="Roboto",
                font_size=14,
                font_weight=BOLD,
                font_style=ITALIC,
            ),
        )

        unknown_style = dict(font_family="Unknown", font_size=14)
        lbl_u = toga.Label("Unknown", style=Pack(**unknown_style))
        lbl_ub = toga.Label(
            "Unknown bold", style=Pack(font_weight=BOLD, **unknown_style)
        )
        lbl_ui = toga.Label(
            "Unknown italic", style=Pack(font_style=ITALIC, **unknown_style)
        )
        lbl_ubi = toga.Label(
            "Unknown bold italic",
            style=Pack(font_weight=BOLD, font_style=ITALIC, **unknown_style),
        )

        self.textpanel = toga.MultilineTextInput(
            readonly=False, style=Pack(flex=1), placeholder="Ready."
        )

        # Outermost box
        outer_box = toga.Box(
            children=[
                btn_box1,
                btn_box2,
                lbl1,
                lbl2,
                lbl3,
                lbl4,
                lbl5,
                lbl6,
                lbl7,
                lbl8,
                lbl_u,
                lbl_ub,
                lbl_ui,
                lbl_ubi,
                self.textpanel,
            ],
            style=Pack(flex=1, direction=COLUMN, padding=10),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleFontExampleApp("Font Example", "org.beeware.widgets.font")


if __name__ == "__main__":
    app = main()
    app.main_loop()
