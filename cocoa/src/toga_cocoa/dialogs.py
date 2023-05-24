from abc import ABC
from pathlib import Path

from .libs import (
    NSURL,
    NSAlert,
    NSAlertFirstButtonReturn,
    NSAlertStyle,
    NSBezelBorder,
    NSFileHandlingPanelOKButton,
    NSFont,
    NSMakeRect,
    NSOpenPanel,
    NSSavePanel,
    NSScrollView,
    NSTextView,
)


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self


class NSAlertDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        alert_style,
        completion_handler,
        on_result=None,
        **kwargs
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        self.native = NSAlert.alloc().init()
        self.native.icon = interface.app.icon._impl.native
        self.native.alertStyle = alert_style
        self.native.messageText = title
        self.native.informativeText = message

        self.build_dialog(**kwargs)

        self.native.beginSheetModalForWindow(
            interface.window._impl.native, completionHandler=completion_handler
        )

    def build_dialog(self):
        pass

    def completion_handler(self, return_value: int) -> None:
        self.on_result(self, None)

        self.interface.future.set_result(None)

    def bool_completion_handler(self, return_value: int) -> None:
        result = return_value == NSAlertFirstButtonReturn

        self.on_result(self, result)

        self.interface.future.set_result(result)


class InfoDialog(NSAlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.completion_handler,
            on_result=on_result,
        )


class QuestionDialog(NSAlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
            on_result=on_result,
        )

    def build_dialog(self):
        self.native.addButtonWithTitle("Yes")
        self.native.addButtonWithTitle("No")


class ConfirmDialog(NSAlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
            on_result=on_result,
        )

    def build_dialog(self):
        self.native.addButtonWithTitle("OK")
        self.native.addButtonWithTitle("Cancel")


class ErrorDialog(NSAlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=self.completion_handler,
            on_result=on_result,
        )


class StackTraceDialog(NSAlertDialog):
    def __init__(self, interface, title, message, on_result=None, **kwargs):
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
            on_result=on_result,
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
        multiselect,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        # Create the panel
        self.create_panel(multiselect)

        # Set all the
        self.panel.title = title

        if filename:
            self.panel.nameFieldStringValue = filename

        if initial_directory:
            self.panel.directoryURL = NSURL.URLWithString(
                str(initial_directory.as_uri())
            )

        self.panel.allowedFileTypes = file_types

        if multiselect:
            handler = self.multi_path_completion_handler
        else:
            handler = self.single_path_completion_handler

        self.panel.beginSheetModalForWindow(
            interface.window._impl.native,
            completionHandler=handler,
        )

    def single_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSFileHandlingPanelOKButton:
            result = Path(self.panel.URL.path)
        else:
            result = None

        self.on_result(self, result)

        self.interface.future.set_result(result)

    def multi_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSFileHandlingPanelOKButton:
            result = [Path(url.path) for url in self.panel.URLs]
        else:
            result = None

        self.on_result(self, result)

        self.interface.future.set_result(result)


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
            multiselect=False,
            on_result=on_result,
        )

    def create_panel(self, multiselect):
        self.panel = NSSavePanel.alloc().init()


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            on_result=on_result,
        )

    def create_panel(self, multiselect):
        self.panel = NSOpenPanel.alloc().init()
        self.panel.allowsMultipleSelection = multiselect
        self.panel.canChooseDirectories = False
        self.panel.canCreateDirectories = False
        self.panel.canChooseFiles = True


class SelectFolderDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiselect=multiselect,
            on_result=on_result,
        )

    def create_panel(self, multiselect):
        self.panel = NSOpenPanel.alloc().init()
        self.panel.allowsMultipleSelection = multiselect
        self.panel.canChooseDirectories = True
        self.panel.canCreateDirectories = True
        self.panel.canChooseFiles = False
        self.panel.resolvesAliases = True
