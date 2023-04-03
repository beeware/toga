import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class FontSize(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        for widget_cls, text_arg, event_name in [
            (toga.Button, "text", "on_press"),
            (toga.Label, "text", None),
            (toga.Switch, "text", "on_change"),
            (toga.TextInput, "value", "on_change"),
        ]:
            main_box.add(row := toga.Box(style=Pack(direction=ROW)))
            for size in [None, 6, 12, 18]:
                style = Pack(flex=1)
                if size:
                    style.font_size = size
                widget = widget_cls(style=style, **{text_arg: str(size)})
                if event_name:
                    setattr(widget, event_name, self.event_handler)
                row.add(widget)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def event_handler(self, widget):
        del widget.style.font_size


def main():
    return FontSize("Font size", "org.beeware.font_size")
