import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class Item(toga.Box):
    def __init__(self, width, text):
        super().__init__(style=Pack(direction=ROW, padding=10, background_color="lime"))

        for x in range(width):
            label = toga.Label(
                text + "," + str(x),
                style=Pack(padding_right=10, background_color="cyan"),
            )
            self.add(label)


class ScrollContainerApp(toga.App):
    TOGGLE_CHUNK = 10

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        self.vswitch = toga.Switch(
            "Vert",
            value=True,
            on_change=self.handle_vscrolling,
        )
        self.hswitch = toga.Switch(
            "Horiz",
            value=False,
            on_change=self.handle_hscrolling,
        )
        self.big_switch = toga.Switch(
            "Big",
            value=True,
            on_change=lambda widget: self.update_content(),
        )
        main_box.add(
            toga.Box(
                style=Pack(direction=ROW),
                children=[self.vswitch, self.hswitch, self.big_switch],
            )
        )

        self.inner_box = toga.Box(
            style=Pack(direction=COLUMN, padding=10, background_color="yellow")
        )
        self.scroller = toga.ScrollContainer(
            horizontal=self.hswitch.value,
            vertical=self.vswitch.value,
            on_scroll=self.on_scroll,
            style=Pack(flex=1, padding=10, background_color="pink"),
        )
        self.update_content()

        self.scroller.content = self.inner_box
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
        self.scroller.horizontal = self.hswitch.value

    def handle_vscrolling(self, widget):
        self.scroller.vertical = self.vswitch.value

    def update_content(self):
        self.inner_box.clear()

        width, height = (10, 50) if self.big_switch.value else (2, 2)
        for x in range(height):
            label_text = f"Label {x}"
            self.inner_box.add(Item(width, label_text))

    def on_scroll(self, scroller):
        self.hswitch.text = "Horiz " + (
            f"({scroller.horizontal_position} / {scroller.max_horizontal_position})"
        )
        self.vswitch.text = "Vert " + (
            f"({scroller.vertical_position} / {scroller.max_vertical_position})"
        )

    def toggle_up(self, widget):
        if not self.vswitch.value:
            return
        try:
            self.scroller.vertical_position -= self.TOGGLE_CHUNK
        except ValueError:
            pass

    def toggle_down(self, widget):
        if not self.vswitch.value:
            return
        try:
            self.scroller.vertical_position += self.TOGGLE_CHUNK
        except ValueError:
            pass

    def toggle_left(self, widget):
        if not self.hswitch.value:
            return
        try:
            self.scroller.horizontal_position -= self.TOGGLE_CHUNK
        except ValueError:
            pass

    def toggle_right(self, widget):
        if not self.hswitch.value:
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
