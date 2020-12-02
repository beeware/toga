# For this example to work under Android, you need a briefcase android template
# which supports onActivityResult in MainActivity.java
# see https://github.com/t-arn/briefcase-android-gradle-template.git branch onActivityResult


import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleFilebrowserApp(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        print("Clicked on 'Do stuff'")
        selected_uri = self.app.main_window.open_file_dialog("Choose a file")
        self.label.text = "You selected: " + str(selected_uri)

    def do_clear(self, widget, **kwargs):
        print('Clearing result')
        self.label.text = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        # Buttons
        btn_style = Pack(flex=1)
        btn_do_stuff = toga.Button('Do stuff', on_press=self.do_stuff, style=btn_style)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)
        btn_box = toga.Box(
            children=[
                btn_do_stuff,
                btn_clear
            ],
            style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
                width=500,
                height=300
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleFilebrowserApp('Filebrowser Demo', 'org.beeware.widgets.filebrowser')


if __name__ == '__main__':
    app = main()
    app.main_loop()
