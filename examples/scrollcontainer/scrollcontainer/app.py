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
    def startup(self):

        box = toga.Box()
        box.style.direction = COLUMN
        box.style.padding = 10

        for x in range(100):
            label_text = 'Label {}'.format(x)
            box.add(Item(label_text))

        scroller = toga.ScrollContainer(horizontal=False)
        scroller.content = box

        self.main_window = toga.MainWindow(self.name)
        self.main_window.content = scroller
        self.main_window.show()


def main():
    return ScrollContainerApp('ScrollContainer', 'org.beeware.widgets.scrollcontainer')


if __name__ == '__main__':
    app = main()
    app.main_loop()
