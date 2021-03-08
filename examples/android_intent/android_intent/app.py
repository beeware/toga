import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleAndroidIntentDemoApp(toga.App):
    Intent = None

    # Button callback functions
    async def do_stuff(self, widget, **kwargs):
        if self.Intent == None:
            from rubicon.java import JavaClass
            self.Intent = JavaClass("android/content/Intent")
        try:
            intent = self.Intent("org.openintents.action.PICK_FILE")
            intent.putExtra("org.openintents.extra.TITLE", "Choose a file")
            result = await self.app._impl.invoke_intent_for_result(intent)
            print(str(result))
            if result["resultData"] is not None:
                selected_file = str(result["resultData"].getData())[7:]
                self.label.text = 'Selected file: ' + selected_file
            else:
                self.label.text = 'No file selected, ResultCode was ' + str(result["resultCode"]) + ")"
        except Exception as ex:
            self.label.text = str(ex)
            self.main_window.info_dialog("Error", "This example requires that 'IO Filemanager' is installed.")

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready')
        if not toga.platform.current_platform == 'android':
            self.label.text = 'This example only works on Android.'

        # Buttons
        btn_style = Pack(flex=1)
        btn_do_stuff = toga.Button('Invoke Intent', on_press=self.do_stuff, style=btn_style)
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
    return ExampleAndroidIntentDemoApp('Android Intent Demo', 'org.beeware.widgets.android_intent')


if __name__ == '__main__':
    app = main()
    app.main_loop()
