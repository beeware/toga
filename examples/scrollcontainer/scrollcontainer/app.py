import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class Item(toga.Box):
    def __init__(self, text):
        super().__init__(style=Pack(direction=COLUMN))

        row = toga.Box(style=Pack(direction=ROW, padding_right=10))

        if toga.platform.current_platform != 'android':  # Divider does not yet exist on Android
            hline = toga.Divider()
            hline.style.padding_top = 5
            hline.style.padding_bottom = 5
            for x in range(1,10):
                label = toga.Label(text+", "+str(x))
                row.add(label)
            self.add(row)
            self.add(hline)
        else:
            for x in range(10):
                label = toga.Label(text+", "+str(x))
                row.add(label)
            self.add(row)


class ScrollContainerApp(toga.App):
    def startup(self):

        box = toga.Box()
        box.style.direction = COLUMN
        box.style.padding = 10

        for x in range(100):
            label_text = 'Label {}'.format(x)
            box.add(Item(label_text))

        scroller = toga.ScrollContainer(horizontal=True, vertical=True)
        scroller.content = box

        self.main_window = toga.MainWindow(self.name, size=(400, 700))
        self.main_window.content = scroller
        self.main_window.show()


def main():
    return ScrollContainerApp('ScrollContainer', 'org.beeware.widgets.scrollcontainer')


if __name__ == '__main__':
    app = main()
    app.main_loop()
