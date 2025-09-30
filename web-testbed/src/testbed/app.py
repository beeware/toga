import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from .web_test_harness import WebTestHarness


class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.label = toga.Label(id="myLabel", text="Test App - Toga Web Testing")

        self.web_test = WebTestHarness(self)

        main_box.add(self.label)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return HelloWorld()
