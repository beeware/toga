import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampledialogsApp(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        self.label.text = "Do stuff."

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def action_info_dialog(self, widget):
        self.main_window.info_dialog('Toga', 'THIS! IS! TOGA!!')

    def action_question_dialog(self, widget):
        if self.main_window.question_dialog('Toga', 'Is this cool or what?'):
            self.main_window.info_dialog('Happiness', 'I know, right! :-)')
        else:
            self.main_window.info_dialog('Shucks...', "Well aren't you a spoilsport... :-(")

    def action_open_file_dialog(self, widget):
        fname = self.main_window.open_file_dialog(
            title="Open file with Toga",
        )
        try:
            self.label.text = "File to open:" + fname
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    def action_select_folder_dialog(self, widget):
        path_name = self.main_window.select_folder_dialog(
            title="Select folder with Toga",
        )
        try:
            self.label.text = "Folder selected:" + path_name
        except ValueError:
            self.label.text = "Folder select dialog was canceled"

    def action_save_file_dialog(self, widget):
        fname = 'Toga_file.txt'
        save_path = self.main_window.save_file_dialog(
            "Save file with Toga",
            suggested_filename=fname)
        if save_path is not None:
            self.label.text = "File saved with Toga:" + fname
        else:
            self.label.text = "Save file dialog was canceled"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.', style=Pack(padding_top=20))

        # Buttons
        btn_style = Pack(flex=1)
        btn_info = toga.Button('Info', on_press=self.action_info_dialog, style=btn_style)
        btn_question = toga.Button('Question', on_press=self.action_question_dialog, style=btn_style)
        btn_open = toga.Button('Open File', on_press=self.action_open_file_dialog, style=btn_style)
        btn_save = toga.Button('Save File', on_press=self.action_save_file_dialog, style=btn_style)
        btn_select = toga.Button('Select Folder', on_press=self.action_select_folder_dialog, style=btn_style)
        dialog_btn_box = toga.Box(
            children=[
                btn_info,
                btn_question,
                btn_open,
                btn_save,
                btn_select
            ],
            style=Pack(direction=ROW)
        )
        # Dialog Buttons
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
            children=[btn_box, dialog_btn_box, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampledialogsApp('Dialogs', 'org.pybee.widgets.dialogs')


if __name__ == '__main__':
    app = main()
    app.main_loop()
