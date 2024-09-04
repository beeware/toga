import asyncio
from pathlib import Path

import toga

from .libs import (
    NSURL,
    NSAlert,
    NSAlertFirstButtonReturn,
    NSAlertStyle,
    NSBezelBorder,
    NSFont,
    NSMakeRect,
    NSModalResponseContinue,
    NSModalResponseOK,
    NSOpenPanel,
    NSSavePanel,
    NSScrollView,
    NSTextView,
)


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        if host_window:
            # Begin the panel window-modal.
            self.host_window = host_window._impl.native
            self.native.beginSheetModalForWindow(
                self.host_window,
                completionHandler=self.completion_handler,
            )
        else:
            # The mechanism for app-modal display depends on the type of dialog.
            self.run_app_modal()


class NSAlertDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        alert_style,
        completion_handler,
        **kwargs,
    ):
        super().__init__()
        self.native = NSAlert.alloc().init()
        self.native.icon = toga.App.app.icon._impl.native
        self.native.alertStyle = alert_style
        self.native.messageText = title
        self.native.informativeText = message

        self.completion_handler = completion_handler

        self.build_dialog(**kwargs)

    def build_dialog(self):
        pass

    def completion_handler(self, return_value: int) -> None:
        self.future.set_result(None)

    def bool_completion_handler(self, return_value: int) -> None:
        self.future.set_result(return_value == NSAlertFirstButtonReturn)

    def _poll_modal_session(self, nsapp, session):
        # This is factored out so it can be mocked for testing purposes.
        return nsapp.runModalSession(session)

    def run_app_modal(self):
        async def _run_app_modal():
            # Begin the NSAlert app-model. Cocoa only provides `-runModal`, which is a
            # blocking method; so we need to build the app-modal equivalent of
            # `-beginSheetModalForWindow:` using primitives and a polling loop.

            # Explicitly force a layout of the alert panel
            self.native.layout()

            # Start the modal loop
            nsapp = toga.App.app._impl.native
            session = nsapp.beginModalSessionForWindow(self.native.window)

            # Poll the modal session, waiting for the dialog to complete
            while (
                result := self._poll_modal_session(nsapp, session)
            ) == NSModalResponseContinue:
                await asyncio.sleep(0.1)

            # End the modal session, handle the result, and hide the dialog
            nsapp.endModalSession(session)
            self.completion_handler(result)
            self.native.window.orderOut(None)

        # This needs to be queued as a background task
        asyncio.create_task(_run_app_modal())


class InfoDialog(NSAlertDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.completion_handler,
        )


class QuestionDialog(NSAlertDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
        )

    def build_dialog(self):
        self.native.addButtonWithTitle("Yes")
        self.native.addButtonWithTitle("No")


class ConfirmDialog(NSAlertDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
        )

    def build_dialog(self):
        self.native.addButtonWithTitle("OK")
        self.native.addButtonWithTitle("Cancel")


class ErrorDialog(NSAlertDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=self.completion_handler,
        )


class StackTraceDialog(NSAlertDialog):
    def __init__(self, title, message, **kwargs):
        if kwargs.get("retry"):
            completion_handler = self.bool_completion_handler
        else:
            completion_handler = self.completion_handler

        super().__init__(
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=completion_handler,
            **kwargs,
        )

    def build_dialog(self, content, retry):
        scroll = NSScrollView.alloc().initWithFrame(NSMakeRect(0, 0, 500, 200))
        scroll.hasVerticalScroller = True
        scroll.hasHorizontalScrolle = False
        scroll.autohidesScrollers = False
        scroll.borderType = NSBezelBorder

        trace = NSTextView.alloc().init()
        trace.insertText(content)
        trace.editable = False
        trace.verticallyResizable = True
        trace.horizontallyResizable = True
        trace.font = NSFont.fontWithName("Menlo", size=12)

        scroll.documentView = trace

        self.native.accessoryView = scroll

        if retry:
            self.native.addButtonWithTitle("Retry")
            self.native.addButtonWithTitle("Quit")


class FileDialog(BaseDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__()

        # Create the panel
        self.create_panel(multiple_select)

        # Set the title of the panel
        self.native.title = title

        if filename:
            self.native.nameFieldStringValue = filename

        if initial_directory:
            self.native.directoryURL = NSURL.URLWithString(
                str(initial_directory.as_uri())
            )

        self.native.allowedFileTypes = file_types

        if multiple_select:
            self.completion_handler = self.multi_path_completion_handler
        else:
            self.completion_handler = self.single_path_completion_handler

    # Provided as a stub that can be mocked in test conditions
    def selected_path(self):
        return self.native.URL

    # Provided as a stub that can be mocked in test conditions
    def selected_paths(self):
        return self.native.URLs

    def single_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSModalResponseOK:
            result = Path(str(self.selected_path().path))
        else:
            result = None

        self.future.set_result(result)

    def multi_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSModalResponseOK:
            result = [Path(url.path) for url in self.selected_paths()]
        else:
            result = None

        self.future.set_result(result)

    def run_app_modal(self):
        self.native.beginWithCompletionHandler(self.completion_handler)


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        super().__init__(
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=None,  # File types aren't offered by Cocoa save panels.
            multiple_select=False,
        )

    def create_panel(self, multiple_select):
        self.native = NSSavePanel.alloc().init()


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__(
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
        )

    def create_panel(self, multiple_select):
        self.native = NSOpenPanel.alloc().init()
        self.native.allowsMultipleSelection = multiple_select
        self.native.canChooseDirectories = False
        self.native.canCreateDirectories = False
        self.native.canChooseFiles = True


class SelectFolderDialog(FileDialog):
    def __init__(
        self,
        title,
        initial_directory,
        multiple_select,
    ):
        super().__init__(
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiple_select=multiple_select,
        )

    def create_panel(self, multiple_select):
        self.native = NSOpenPanel.alloc().init()
        self.native.allowsMultipleSelection = multiple_select
        self.native.canChooseDirectories = True
        self.native.canCreateDirectories = True
        self.native.canChooseFiles = False
        self.native.resolvesAliases = True
