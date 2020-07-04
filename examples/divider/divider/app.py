import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class DividerApp(toga.App):

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(title=self.name, size=(300, 150))

        style = Pack(padding_top=24)
        substyle = Pack(padding_right=24, flex=1)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                toga.Label('Section 1'),
                toga.Divider(style=style),
                toga.Label('Section 2', style=style),
                toga.Divider(style=style),
                toga.Label('Section 3', style=style),
                toga.Box(
                    children=[
                        toga.DetailedList(['List 1'], style=substyle),
                        toga.Divider(direction=toga.Divider.VERTICAL, style=substyle),
                        toga.DetailedList(['List 2'], style=substyle),
                    ],
                    style=Pack(direction=ROW, padding=24, flex=1),
                ),
            ],
            style=Pack(direction=COLUMN, padding=24)
        )

        # Show the main window
        self.main_window.show()


def main():
    # Application class
    #   App name and namespace
    app = DividerApp('Dividers', 'org.beeware.helloworld')
    return app
