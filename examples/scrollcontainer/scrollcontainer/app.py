import toga
from toga.constants import COLUMN, LEFT
from toga.style import Pack


class ScrollContainerApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(self.name)
        box = toga.Box()
        box.style.direction = COLUMN

        for x in range(100):
            label_text = 'Label %d' % (x)
            box.add(toga.Label(label_text, style=Pack(text_align=LEFT)))

        scroller = toga.ScrollContainer()
        scroller.content = box

        self.main_window.content = scroller
        self.main_window.show()


def main():
    return ScrollContainerApp('ScrollContainer', 'org.beeware.widgets.scrollcontainer')


if __name__ == '__main__':
    app = main()
    app.main_loop()
