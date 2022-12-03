import toga


class TogaTest(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box()
        self.main_window.show()


def main():
    return TogaTest(app_name="toga_test")
