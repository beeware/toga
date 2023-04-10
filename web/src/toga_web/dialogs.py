import asyncio

from toga_web.libs import create_element, js


class BaseDialog:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

    def __eq__(self, other):
        raise RuntimeError(
            "Can't check dialog result directly; use await or an on_result handler"
        )

    def __bool__(self):
        raise RuntimeError(
            "Can't check dialog result directly; use await or an on_result handler"
        )

    def __await__(self):
        return self.future.__await__()


class InfoDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__()
        self.native = create_element(
            "sl-dialog",
            id="toga-info-dialog",
            label=title,
            children=[
                create_element("p", content=message),
            ]
            + self.create_buttons(),
        )

        # Add the dialog to the DOM.
        window.app._impl.native.appendChild(self.native)

        # If this is the first time a dialog is being shown, the Shoelace
        # autoloader needs to construct the Dialog custom element. We can't
        # display the dialog until that element has been fully loaded and
        # cosntructed. Only show the dialog when the promise of <sl-dialog>
        # element construction has been fulfilled.
        js.customElements.whenDefined("sl-dialog").then(self.show_dialog)

    def create_buttons(self):
        close_button = create_element(
            "sl-button", slot="footer", variant="primary", content="Ok"
        )
        # Handle the close of the dialog
        close_button.onclick = self.dialog_close

        return [close_button]

    def show_dialog(self, promise):
        self.native.show()

    def dialog_close(self, event):
        self.native.hide()
        self.native.parentElement.removeChild(self.native)
        self.future.set_result(None)


class QuestionDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__()

        # TODO: Replace with something more customized using Bootstrap modals.
        self.future.set_result(js.confirm(message))


class ConfirmDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__()

        # TODO: Replace with something more customized using Bootstrap modals.
        self.future.set_result(js.confirm(message))


class ErrorDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__()

        # TODO: Replace with something more customized using Bootstrap modals.
        self.future.set_result(js.alert(message))


class StackTraceDialog:
    def __init__(self, window, title, message, on_result=None, **kwargs):
        super().__init__()
        # TODO: Replace with something more customized using Bootstrap modals.
        if kwargs.get("retry"):
            self.future.set_result(
                js.confirm("Stack trace: \n\n:" + message + "\n\nRetry?")
            )
        else:
            self.future.set_result(js.alert("Stack trace: \n\n:" + message))


class SaveFileDialog:
    def __init__(
        self,
        window,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        window.factory.not_implemented("Window.save_file_dialog()")


class OpenFileDialog:
    def __init__(
        self, window, title, initial_directory, file_types, multiselect, on_result=None
    ):
        window.factory.not_implemented("Window.open_file_dialog()")


class SelectFolderDialog:
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        window.factory.not_implemented("Window.select_folder_dialog()")
