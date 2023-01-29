import toga


class Testbed(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(
            children=[
                toga.Label("Did you forget to use --test?"),
            ]
        )
        self.main_window.show()


def main():
    return Testbed(app_name="testbed")
