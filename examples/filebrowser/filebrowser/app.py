# For this example to work under Android, you need a briefcase android template
# which supports onActivityResult in MainActivity.java
# see https://github.com/t-arn/briefcase-android-gradle-template.git branch onActivityResult


import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleFilebrowserApp(toga.App):
    # Button callback functions
    async def do_open_file(self, widget, **kwargs):
        print("Clicked on 'Open file'")
        multiselect = False
        if self.multiselect.value == 'True':
            multiselect = True
        selected_uri = await self.app.main_window.open_file_dialog("Choose a file", self.initial_dir.value, self.file_types.value, multiselect)
        self.multiline.value = "You selected: \n" + str(selected_uri)

    def do_clear(self, widget, **kwargs):
        print('Clearing result')
        self.multiline.value = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        flex_style = Pack(flex=1)

        # set options
        self.initial_dir = toga.TextInput(placeholder='initial directory', style=flex_style)
        self.file_types = toga.TextInput(placeholder='file types', style=flex_style)
        self.multiselect = toga.TextInput(placeholder='is multiselect? (True / False)', style=flex_style)
        self.folder = toga.TextInput(placeholder='what to select? (file / folder)', style=flex_style)
        # Toga.Switch does not seem to work on Android ...
        # self.multiselect = toga.Switch('multiselect', is_on=False)
        # self.folder = toga.Switch('select folder')

        # Text field to show responses.
        self.multiline = toga.MultilineTextInput('Ready.', style=flex_style)

        # Buttons
        btn_open_file = toga.Button('Open file', on_press=self.do_open_file, style=flex_style)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=flex_style)
        btn_box = toga.Box(
            children=[
                btn_open_file,
                btn_clear
            ],
            style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.initial_dir, self.file_types, self.multiselect, self.folder, btn_box, self.multiline],
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
