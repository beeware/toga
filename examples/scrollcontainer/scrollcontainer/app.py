import toga
from toga.constants import COLUMN
from toga.style import Pack


class Item(toga.Box):
    def __init__(self, text):
        super().__init__(style=Pack(direction=COLUMN))

        label = toga.Label(text)

        hline = toga.Divider()
        hline.style.padding_top = 5
        hline.style.padding_bottom = 5

        self.add(label, hline)


class ScrollContainerApp(toga.App):
    TOGGLE_CHUNK = 0.1

    def startup(self):
        self.top_label = toga.Label("I'm top", style=Pack(width=100))
        top_box = toga.Box(children=[self.top_label])
        self.scroller = toga.ScrollContainer(horizontal=False, on_scroll=self.on_scroll)
        self.scroller.content = self.build_items_box()

        self.main_window = toga.MainWindow(self.name)
        self.main_window.content = toga.Box(
            children=[top_box, self.scroller],
            style=Pack(direction=COLUMN)
        )
        self.main_window.show()

        self.commands.add(
            toga.Command(
                self.toggle_up,
                "Toggle Up",
                shortcut=toga.Key.MOD_1 + toga.Key.UP,
                group=toga.Group.COMMANDS
            ),
            toga.Command(
                self.toggle_down,
                "Toggle DOWN",
                shortcut=toga.Key.MOD_1 + toga.Key.DOWN,
                group=toga.Group.COMMANDS
            )
        )

    @classmethod
    def build_items_box(cls):
        box = toga.Box()
        box.style.direction = COLUMN
        box.style.padding = 10
        for x in range(100):
            label_text = 'Label {}'.format(x)
            box.add(Item(label_text))
        return box

    def on_scroll(self, widget):
        self.top_label.text = "I'm at {:.2f}".format(self.scroller.vertical_position)

    def toggle_up(self, widget):
        if self.scroller.vertical_position > self.TOGGLE_CHUNK:
            self.scroller.vertical_position -= self.TOGGLE_CHUNK

    def toggle_down(self, widget):
        if self.scroller.vertical_position < 1 - self.TOGGLE_CHUNK:
            self.scroller.vertical_position += self.TOGGLE_CHUNK


def main():
    return ScrollContainerApp('ScrollContainer', 'org.beeware.widgets.scrollcontainer')


if __name__ == '__main__':
    app = main()
    app.main_loop()
