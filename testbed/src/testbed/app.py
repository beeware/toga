import toga


class Testbed(toga.App):
    def startup(self):
        # A flag that controls whether the test suite should slow down
        # so that changes are observable
        self.run_slow = False

        # Set a default return code for the app, so that a value is
        # available if the app exits for a reason other than the test
        # suite exiting/crashing.
        self.returncode = -1

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(
            children=[
                toga.Label("Did you forget to use --test?"),
            ]
        )
        self.main_window.show()


def main():
    return Testbed(app_name="testbed")
