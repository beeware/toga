import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class Item(toga.Box):
    def __init__(self, text):
        super().__init__(style=Pack(direction=COLUMN))

        row = toga.Box(style=Pack(direction=ROW))
        for x in range(10):
            label = toga.Label(text + ", " + str(x), style=Pack(padding_right=10))
            row.add(label)
        self.add(row)


class ScrollContainerApp(toga.App):
    TOGGLE_CHUNK = 10

    vscrolling = True
    hscrolling = False
    scroller = None

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        self.vswitch = toga.Switch(
            "Vertical",
            value=self.vscrolling,
            on_change=self.handle_vscrolling,
        )
        self.hswitch = toga.Switch(
            "Horizontal",
            value=self.hscrolling,
            on_change=self.handle_hscrolling,
        )
        main_box.add(
            toga.Box(style=Pack(direction=ROW), children=[self.vswitch, self.hswitch])
        )

        box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.scroller = toga.ScrollContainer(
            horizontal=self.hscrolling,
            vertical=self.vscrolling,
            on_scroll=self.on_scroll,
            style=Pack(flex=1),
        )

        for x in range(100):
            label_text = f"Label {x}"
            box.add(Item(label_text))

        self.scroller.content = box
        main_box.add(self.scroller)

        self.main_window = toga.MainWindow(self.name, size=(400, 700))
        self.main_window.content = main_box
        self.main_window.show()

        self.commands.add(
            toga.Command(
                self.toggle_up,
                "Toggle Up",
                shortcut=toga.Key.MOD_1 + toga.Key.UP,
                group=toga.Group.COMMANDS,
                order=1,
            ),
            toga.Command(
                self.toggle_down,
                "Toggle Down",
                shortcut=toga.Key.MOD_1 + toga.Key.DOWN,
                group=toga.Group.COMMANDS,
                order=2,
            ),
            toga.Command(
                self.toggle_left,
                "Toggle Left",
                shortcut=toga.Key.MOD_1 + toga.Key.LEFT,
                group=toga.Group.COMMANDS,
                order=3,
            ),
            toga.Command(
                self.toggle_right,
                "Toggle Right",
                shortcut=toga.Key.MOD_1 + toga.Key.RIGHT,
                group=toga.Group.COMMANDS,
                order=4,
            ),
        )

    def handle_hscrolling(self, widget):
        self.hscrolling = widget.value
        self.scroller.horizontal = self.hscrolling

    def handle_vscrolling(self, widget):
        self.vscrolling = widget.value
        self.scroller.vertical = self.vscrolling

    def on_scroll(self, scroller):
        self.hswitch.text = "Horizontal " + (
            f"({scroller.horizontal_position} / {scroller.max_horizontal_position})"
        )
        self.vswitch.text = "Vertical " + (
            f"({scroller.vertical_position} / {scroller.max_vertical_position})"
        )

    def toggle_up(self, widget):
        if not self.vscrolling:
            return
        try:
            self.scroller.vertical_position -= self.TOGGLE_CHUNK
        except ValueError:
            pass

    def toggle_down(self, widget):
        if not self.vscrolling:
            return
        try:
            self.scroller.vertical_position += self.TOGGLE_CHUNK
        except ValueError:
            pass

    def toggle_left(self, widget):
        if not self.hscrolling:
            return
        try:
            self.scroller.horizontal_position -= self.TOGGLE_CHUNK
        except ValueError:
            pass

    def toggle_right(self, widget):
        if not self.hscrolling:
            return
        try:
            self.scroller.horizontal_position += self.TOGGLE_CHUNK
        except ValueError:
            pass


def main():
    return ScrollContainerApp("ScrollContainer", "org.beeware.widgets.scrollcontainer")


if __name__ == "__main__":
    app = main()
    app.main_loop()
