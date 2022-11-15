import pytest
import tests

import toga


class TogaTest(toga.App):
    def startup(self):
        # For the "app" fixture.
        global app
        app = self

        self.main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        self.add_background_task(test)


def test(app):
    pytest.main(["-vv", "--color=no"] + tests.__path__)


def main():
    return TogaTest()
