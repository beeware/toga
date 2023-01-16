import traceback
from pathlib import Path

import toga
from toga.constants import COLUMN
from toga.style import Pack


class ExampledialogsApp(toga.App):
    # Button callback functions
    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    async def action_info_dialog(self, widget):
        await self.main_window.info_dialog("Toga", "THIS! IS! TOGA!!")
        self.label.text = "Information was provided."

    async def action_question_dialog(self, widget):
        if await self.main_window.question_dialog("Toga", "Is this cool or what?"):
            self.label.text = "User said yes!"
            await self.main_window.info_dialog("Happiness", "I know, right! :-)")
        else:
            self.label.text = "User says no..."
            await self.main_window.info_dialog(
                "Shucks...", "Well aren't you a spoilsport... :-("
            )

    async def action_confirm_dialog(self, widget):
        if await self.main_window.question_dialog("Toga", "Are you sure you want to?"):
            self.label.text = "Lets do it!"
        else:
            self.label.text = "Left it as it was."

    async def action_error_dialog(self, widget):
        await self.main_window.error_dialog(
            "Toga", "Well that didn't work... or did it?"
        )
        self.label.text = "Oh noes..."

    async def action_stack_trace(self, widget):
        await self.main_window.stack_trace_dialog(
            "Well that wasn't good",
            "Here's where you were when it went bad:",
            "".join(traceback.format_stack()),
        )
        self.label.text = "Stack traced..."

    async def action_stack_trace_retry(self, widget):
        retry = await self.main_window.stack_trace_dialog(
            "Want a do-over?",
            "Here's where you were when it went bad:",
            "".join(traceback.format_stack()),
            retry=True,
        )
        if retry:
            self.label.text = "Lets try that again..."
        else:
            self.label.text = "Quit while you're ahead..."

    async def action_open_file_dialog(self, widget):
        try:
            fname = await self.main_window.open_file_dialog(
                title="Open file with Toga", multiselect=False
            )
            if fname is not None:
                self.label.text = f"File to open: {fname}"
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    async def action_open_file_filtered_dialog(self, widget):
        try:
            fname = await self.main_window.open_file_dialog(
                title="Open file with Toga",
                multiselect=False,
                file_types=["doc", "txt"],
            )
            if fname is not None:
                self.label.text = f"File to open: {fname}"
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    async def action_open_file_dialog_multi(self, widget):
        try:
            filenames = await self.main_window.open_file_dialog(
                title="Open file with Toga", multiselect=True
            )
            if filenames is not None:
                msg = f"Files to open: {', '.join(str(f) for f in filenames)}"
                self.label.text = msg
            else:
                self.label.text = "No files selected!"

        except ValueError:
            self.label.text = "Open file dialog was canceled"

    async def action_open_file_dialog_with_inital_folder(self, widget):
        try:
            fname = await self.main_window.open_file_dialog(
                title="Open file with Toga in home folder",
                initial_directory=Path.home(),
                multiselect=False,
            )
            if fname is not None:
                self.label.text = f"File to open: {fname}"
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    async def action_select_folder_dialog(self, widget):
        try:
            path_name = await self.main_window.select_folder_dialog(
                title="Select folder with Toga"
            )
            if path_name is not None:
                self.label.text = f"Folder selected: {path_name}"
            else:
                self.label.text = "No folder selected!"
        except ValueError:
            self.label.text = "Folder select dialog was canceled"

    async def action_select_folder_dialog_multi(self, widget):
        try:
            path_names = await self.main_window.select_folder_dialog(
                title="Select multiple folders with Toga", multiselect=True
            )
            if path_names is not None:
                self.label.text = (
                    f"Folders selected: {','.join([str(p) for p in path_names])}"
                )
            else:
                self.label.text = "No fodlers selected!"
        except ValueError:
            self.label.text = "Folders select dialog was canceled"

    async def action_select_folder_dialog_with_initial_folder(self, widget):
        try:
            path_name = await self.main_window.select_folder_dialog(
                title="Select folder with Toga in current folder",
                initial_directory=Path.cwd(),
            )
            self.label.text = f"Folder selected: {path_name}"
        except ValueError:
            self.label.text = "Folder select dialog was canceled"

    async def action_save_file_dialog(self, widget):
        fname = "Toga_file.txt"
        try:
            save_path = await self.main_window.save_file_dialog(
                "Save file with Toga",
                suggested_filename=fname,
            )
            if save_path is not None:
                self.label.text = f"File saved with Toga: {save_path}"
            else:
                self.label.text = "Save file dialog was canceled"

        except ValueError:
            self.label.text = "Save file dialog was canceled"

    async def window_close_handler(self, window):
        # This handler is called before the window is closed, so there
        # still are 1 more windows than the number of secondary windows
        # after it is closed
        # Return False if the window should stay open

        # Check to see if there has been a previous close attempt.
        if window in self.close_attempts:
            # If there has, update the window label and allow
            # the close to proceed. The count is -2 (rather than -1)
            # because *this* window hasn't been removed from
            # the window list.
            self.set_window_label_text(len(self.windows) - 2)
            return True
        else:
            await window.info_dialog(
                f"Abort {window.title}!", "Maybe try that again..."
            )
            self.close_attempts.add(window)
            return False

    def action_open_secondary_window(self, widget):
        self.window_counter += 1
        window = toga.Window(title=f"New Window {self.window_counter}")
        # Both self.windows.add() and self.windows += work:
        self.windows += window

        self.set_window_label_text(len(self.windows) - 1)
        secondary_label = toga.Label(text="You are in a secondary window!")
        window.content = toga.Box(
            children=[secondary_label], style=Pack(flex=1, direction=COLUMN, padding=10)
        )
        window.on_close = self.window_close_handler
        window.show()

    def action_close_secondary_windows(self, widget):
        # Close all windows that aren't the main window.
        for window in list(self.windows):
            if not isinstance(window, toga.MainWindow):
                window.close()

    async def exit_handler(self, app):
        # Return True if app should close, and False if it should remain open
        if await self.main_window.confirm_dialog(
            "Toga", "Are you sure you want to quit?"
        ):
            print(f"Label text was '{self.label.text}' when you quit the app")
            return True
        else:
            self.label.text = "Exit canceled"
            return False

    def set_window_label_text(self, num_windows):
        self.window_label.text = f"{num_windows} secondary window(s) open"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)
        self.on_exit = self.exit_handler

        # Label to show responses.
        self.label = toga.Label("Ready.", style=Pack(padding_top=20))
        self.window_label = toga.Label("", style=Pack(padding_top=20))
        self.window_counter = 0
        self.close_attempts = set()
        self.set_window_label_text(0)

        # Buttons
        btn_style = Pack(flex=1)
        btn_info = toga.Button(
            "Info", on_press=self.action_info_dialog, style=btn_style
        )
        btn_question = toga.Button(
            "Question", on_press=self.action_question_dialog, style=btn_style
        )
        btn_confirm = toga.Button(
            "Confirm", on_press=self.action_confirm_dialog, style=btn_style
        )
        btn_error = toga.Button(
            "Error", on_press=self.action_error_dialog, style=btn_style
        )
        btn_stack_trace = toga.Button(
            "Stack Trace", on_press=self.action_stack_trace, style=btn_style
        )
        btn_stack_trace_retry = toga.Button(
            "Stack Trace (with retry)",
            on_press=self.action_stack_trace_retry,
            style=btn_style,
        )
        btn_open = toga.Button(
            "Open File", on_press=self.action_open_file_dialog, style=btn_style
        )
        btn_open_filtered = toga.Button(
            "Open File (Filtered)",
            on_press=self.action_open_file_filtered_dialog,
            style=btn_style,
        )
        btn_open_multi = toga.Button(
            "Open File (Multiple)",
            on_press=self.action_open_file_dialog_multi,
            style=btn_style,
        )
        btn_open_init_folder = toga.Button(
            "Open File In Home Folder",
            on_press=self.action_open_file_dialog_with_inital_folder,
        )

        btn_save = toga.Button(
            "Save File", on_press=self.action_save_file_dialog, style=btn_style
        )
        btn_select = toga.Button(
            "Select Folder", on_press=self.action_select_folder_dialog, style=btn_style
        )
        btn_select_multi = toga.Button(
            "Select Folders",
            on_press=self.action_select_folder_dialog_multi,
            style=btn_style,
        )
        btn_select_init_folder = toga.Button(
            "Select Folder In Current Folder ",
            on_press=self.action_select_folder_dialog_with_initial_folder,
            style=btn_style,
        )

        btn_open_secondary_window = toga.Button(
            "Open Secondary Window",
            on_press=self.action_open_secondary_window,
            style=btn_style,
        )
        btn_close_secondary_window = toga.Button(
            "Close All Secondary Windows",
            on_press=self.action_close_secondary_windows,
            style=btn_style,
        )

        btn_clear = toga.Button("Clear", on_press=self.do_clear, style=btn_style)

        # Outermost box
        box = toga.Box(
            children=[
                btn_info,
                btn_question,
                btn_confirm,
                btn_error,
                btn_stack_trace,
                btn_stack_trace_retry,
                btn_open,
                btn_open_filtered,
                btn_open_multi,
                btn_open_init_folder,
                btn_save,
                btn_select,
                btn_select_multi,
                btn_select_init_folder,
                btn_open_secondary_window,
                btn_close_secondary_window,
                btn_clear,
                self.label,
                self.window_label,
            ],
            style=Pack(flex=1, direction=COLUMN, padding=10),
        )

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()


def main():
    return ExampledialogsApp("Dialogs", "org.beeware.widgets.dialogs")


if __name__ == "__main__":
    app = main()
    app.main_loop()
