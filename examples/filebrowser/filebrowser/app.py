# For this example to work under Android, you need a briefcase android template
# which supports onActivityResult in MainActivity.java
# see https://github.com/t-arn/briefcase-android-gradle-template.git branch onActivityResult


import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
from rubicon.java import JavaClass

Intent = JavaClass("android/content/Intent")
Activity = JavaClass("android/app/Activity")


class ExampleFilebrowserApp(toga.App):
    # Button callback functions
    async def do_open_file(self, widget, **kwargs):
        print("Clicked on 'Open file'")
        multiselect = False
        mimetypes = str(self.file_types.value).split(' ')
        if self.multiselect.value == 'True':
            multiselect = True
        try:
            selected_uri = ''
            if self.use_oifm.value != 'True':
                selected_uri = await self.app.main_window.open_file_dialog("Choose a file", self.initial_dir.value,
                                                                           mimetypes, multiselect)
            else:
                intent = Intent("org.openintents.action.PICK_FILE")
                intent.putExtra("org.openintents.extra.TITLE", "Choose a file")
                result = await self.app._impl.invoke_intent_for_result(intent)
                print(str(result))
                if result["resultData"] is not None:
                    selected_uri = result["resultData"].getData()
                else:
                    selected_uri = 'No file selected, ResultCode was ' + str(result["resultCode"]) + ")"
        except ValueError as e:
            selected_uri = str(e)
        print(str(selected_uri))
        self.multiline.value = "You selected: \n" + str(selected_uri)

    async def do_open_folder(self, widget, **kwargs):
        print("Clicked on 'Open folder'")
        multiselect = False
        if self.multiselect.value == 'True':
            multiselect = True
        try:
            selected_uri = ''
            if self.use_oifm.value != 'True':
                selected_uri = await self.app.main_window.select_folder_dialog("Choose a folder",
                                                                               self.initial_dir.value, multiselect)
            else:
                intent = Intent("org.openintents.action.PICK_DIRECTORY")
                intent.putExtra("org.openintents.extra.TITLE", "Choose a folder")
                result = await self.app._impl.invoke_intent_for_result(intent)
                print(str(result))
                if result["resultData"] is not None:
                    selected_uri = result["resultData"].getData()
                else:
                    selected_uri = 'No folder selected, ResultCode was ' + str(result["resultCode"]) + ")"
        except ValueError as e:
            selected_uri = str(e)
        self.multiline.value = "You selected: \n" + str(selected_uri)

    def do_clear(self, widget, **kwargs):
        print('Clearing result')
        self.multiline.value = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(400, 700))
        flex_style = Pack(flex=1)

        # set options
        self.initial_dir = toga.TextInput(placeholder='initial directory', style=flex_style)
        self.file_types = toga.TextInput(placeholder='MIME types (blank separated)', style=flex_style)
        self.multiselect = toga.TextInput(placeholder='is multiselect? (True / False)', style=flex_style)
        self.use_oifm = toga.TextInput(placeholder='Use OI Filemanager? (True / False)', style=flex_style)
        # Toga.Switch does not seem to work on Android ...
        # self.multiselect = toga.Switch('multiselect', is_on=False)
        # self.use_oifm = toga.Switch('Use OI Filemanager')

        # Text field to show responses.
        self.multiline = toga.MultilineTextInput('Ready.', style=(Pack(height=200)))

        # Buttons
        btn_open_file = toga.Button('Open file', on_press=self.do_open_file, style=flex_style)
        btn_open_folder = toga.Button('Open folder', on_press=self.do_open_folder, style=flex_style)
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=flex_style)
        btn_box = toga.Box(
            children=[
                btn_open_file,
                btn_open_folder,
                btn_clear
            ],
            style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.initial_dir, self.file_types, self.multiselect, self.use_oifm, btn_box, self.multiline],
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
    return ExampleFilebrowserApp('Android Filebrowser Demo', 'org.beeware.widgets.filebrowser')


if __name__ == '__main__':
    app = main()
    app.main_loop()
