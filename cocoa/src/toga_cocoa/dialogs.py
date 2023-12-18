from abc import ABC
from pathlib import Path

from .libs import (
    NSURL,
    NSAlert,
    NSAlertFirstButtonReturn,
    NSAlertStyle,
    NSBezelBorder,
    NSFont,
    NSMakeRect,
    NSModalResponseOK,
    NSOpenPanel,
    NSSavePanel,
    NSScrollView,
    NSTextView,
)


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


class NSAlertDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        alert_style,
        completion_handler,
        **kwargs,
    ):
        super().__init__(interface=interface)

        self.native = NSAlert.alloc().init()
        self.native.icon = interface.app.icon._impl.native
        self.native.alertStyle = alert_style
        self.native.messageText = title
        self.native.informativeText = message

        self.build_dialog(**kwargs)

        self.native.beginSheetModalForWindow(
            interface.window._impl.native,
            completionHandler=completion_handler,
        )

    def build_dialog(self):
        pass

    def completion_handler(self, return_value: int) -> None:
        self.interface.set_result(None)

    def bool_completion_handler(self, return_value: int) -> None:
        self.interface.set_result(return_value == NSAlertFirstButtonReturn)


class InfoDialog(NSAlertDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.completion_handler,
        )


class QuestionDialog(NSAlertDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
        )

    def build_dialog(self):
        self.native.addButtonWithTitle("Yes")
        self.native.addButtonWithTitle("No")


class ConfirmDialog(NSAlertDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
        )

    def build_dialog(self):
        self.native.addButtonWithTitle("OK")
        self.native.addButtonWithTitle("Cancel")


class ErrorDialog(NSAlertDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=self.completion_handler,
        )


class StackTraceDialog(NSAlertDialog):
    def __init__(self, interface, title, message, **kwargs):
        if kwargs.get("retry"):
            completion_handler = self.bool_completion_handler
        else:
            completion_handler = self.completion_handler

        super().__init__(
            interface=interface,
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
        interface,
        title,
        filename,
        initial_directory,
        file_types,
        multiple_select,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

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
            handler = self.multi_path_completion_handler
        else:
            handler = self.single_path_completion_handler

        self.native.beginSheetModalForWindow(
            interface.window._impl.native,
            completionHandler=handler,
        )

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

        self.interface.set_result(result)

    def multi_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSModalResponseOK:
            result = [Path(url.path) for url in self.selected_paths()]
        else:
            result = None

        self.interface.set_result(result)


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
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
        interface,
        title,
        initial_directory,
        file_types,
        multiple_select,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
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
        interface,
        title,
        initial_directory,
        multiple_select,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
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
