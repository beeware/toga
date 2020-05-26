import toga
from toga.constants import COLUMN
from toga.style import Pack


class ExampledialogsApp(toga.App):
    # Button callback functions
    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def action_info_dialog(self, widget):
        self.main_window.info_dialog('Toga', 'THIS! IS! TOGA!!')
        self.label.text = 'Information was provided.'

    def action_question_dialog(self, widget):
        if self.main_window.question_dialog('Toga', 'Is this cool or what?'):
            self.label.text = 'User said yes!'
            self.main_window.info_dialog('Happiness', 'I know, right! :-)')
        else:
            self.label.text = 'User says no...'
            self.main_window.info_dialog('Shucks...', "Well aren't you a spoilsport... :-(")

    def action_confirm_dialog(self, widget):
        if self.main_window.question_dialog('Toga', 'Are you sure you want to?'):
            self.label.text = 'Lets do it!'
        else:
            self.label.text = "Left it as it was."

    def action_error_dialog(self, widget):
        self.main_window.error_dialog('Toga', "Well that didn't work... or did it?")
        self.label.text = 'Oh noes...'

    def action_open_file_dialog(self, widget):
        try:
            fname = self.main_window.open_file_dialog(
                title="Open file with Toga",
                multiselect=False
            )
            if fname is not None:
                self.label.text = "File to open:" + fname
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    def action_open_file_dialog_multi(self, widget):
        try:
            filenames = self.main_window.open_file_dialog(
                title="Open file with Toga",
                multiselect=True
            )
            if filenames is not None:
                msg = "Files to open: {}".format(', '.join(filenames))
                self.label.text = msg
            else:
                self.label.text = "No files selected!"

        except ValueError:
            self.label.text = "Open file dialog was canceled"

    def action_select_folder_dialog(self, widget):
        try:
            path_names = self.main_window.select_folder_dialog(
                title="Select folder with Toga"
            )
            self.label.text = "Folder selected:" + ','.join([path for path in path_names])
        except ValueError:
            self.label.text = "Folder select dialog was canceled"

    def action_select_folder_dialog_multi(self, widget):
        try:
            path_names = self.main_window.select_folder_dialog(
                title="Select multiple folders with Toga",
                multiselect=True
            )
            self.label.text = "Folders selected:" + ','.join([path for path in path_names])
        except ValueError:
            self.label.text = "Folders select dialog was canceled"

    def action_save_file_dialog(self, widget):
        fname = 'Toga_file.txt'
        try:
            save_path = self.main_window.save_file_dialog(
                "Save file with Toga",
                suggested_filename=fname)
            if save_path is not None:
                self.label.text = "File saved with Toga:" + save_path
            else:
                self.label.text = "Save file dialog was canceled"
        except ValueError:
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
        btn_confirm = toga.Button('Confirm', on_press=self.action_confirm_dialog, style=btn_style)
        btn_error = toga.Button('Error', on_press=self.action_error_dialog, style=btn_style)
        btn_open = toga.Button('Open File', on_press=self.action_open_file_dialog, style=btn_style)
        btn_open_multi = toga.Button(
            'Open File (Multiple)',
            on_press=self.action_open_file_dialog_multi,
            style=btn_style
        )
        btn_save = toga.Button('Save File', on_press=self.action_save_file_dialog, style=btn_style)
        btn_select = toga.Button('Select Folder', on_press=self.action_select_folder_dialog, style=btn_style)
        btn_select_multi = toga.Button(
            'Select Folders',
            on_press=self.action_select_folder_dialog_multi,
            style=btn_style
        )

        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)

        # Outermost box
        box = toga.Box(
            children=[
                btn_info,
                btn_question,
                btn_confirm,
                btn_error,
                btn_open,
                btn_save,
                btn_select,
                btn_select_multi,
                btn_open_multi,
                btn_clear,
                self.label
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10
            )
        )

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()


def main():
    return ExampledialogsApp('Dialogs', 'org.beeware.widgets.dialogs')


if __name__ == '__main__':
    app = main()
    app.main_loop()
