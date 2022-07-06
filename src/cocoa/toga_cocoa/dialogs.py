import asyncio
from pathlib import Path

from .libs import (
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
    NSURL,
)


class BaseDialog:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

    def __eq__(self, other):
        raise RuntimeError("Can't check dialog result directly; use await or an on_result handler")

    def __bool__(self):
        raise RuntimeError("Can't check dialog result directly; use await or an on_result handler")

    def __await__(self):
        return self.future.__await__()


class NSAlertDialog(BaseDialog):
    def __init__(self, window, title, message, alert_style, completion_handler, on_result=None, **kwargs):
        super().__init__()
        self.on_result = on_result

        alert = NSAlert.alloc().init()
        alert.icon = window.app.icon._impl.native
        alert.alertStyle = alert_style
        alert.messageText = title
        alert.informativeText = message

        self.build_dialog(alert, **kwargs)

        alert.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    def build_dialog(self, alert):
        pass

    def completion_handler(self, return_value: int) -> None:
        if self.on_result:
            self.on_result(self, None)

        self.future.set_result(None)

    def bool_completion_handler(self, return_value: int) -> None:
        result = return_value == NSAlertFirstButtonReturn

        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)


class InfoDialog(NSAlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.completion_handler,
            on_result=on_result,
        )


class QuestionDialog(NSAlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
            on_result=on_result,
        )

    def build_dialog(self, alert):
        alert.addButtonWithTitle("Yes")
        alert.addButtonWithTitle("No")


class ConfirmDialog(NSAlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Informational,
            completion_handler=self.bool_completion_handler,
            on_result=on_result,
        )

    def build_dialog(self, alert):
        alert.addButtonWithTitle("OK")
        alert.addButtonWithTitle("Cancel")


class ErrorDialog(NSAlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=self.completion_handler,
            on_result=on_result,
        )


class StackTraceDialog(NSAlertDialog):
    def __init__(self, window, title, message, on_result=None, **kwargs):
        if kwargs.get("retry"):
            completion_handler = self.bool_completion_handler
        else:
            completion_handler = self.completion_handler

        super().__init__(
            window=window,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=completion_handler,
            on_result=on_result,
            **kwargs,
        )

    def build_dialog(self, alert, content, retry):
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

        alert.accessoryView = scroll

        if retry:
            alert.addButtonWithTitle("Retry")
            alert.addButtonWithTitle("Quit")


class FileDialog(BaseDialog):
    def __init__(self, window, title, filename, initial_directory, file_types, multiselect, on_result=None):
        super().__init__()
        self.on_result = on_result

        # Create the panel
        self.create_panel(multiselect)

        # Set all the
        self.panel.title = title

        if filename:
            self.panel.nameFieldStringValue = filename

        if initial_directory:
            self.panel.directoryURL = NSURL.URLWithString(str(initial_directory.as_uri()))

        self.panel.allowedFileTypes = file_types

        if multiselect:
            handler = self.multi_path_completion_handler
        else:
            handler = self.single_path_completion_handler

        self.panel.beginSheetModalForWindow(
            window._impl.native,
            completionHandler=handler,
        )

    def single_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSFileHandlingPanelOKButton:
            result = Path(self.panel.URL.path)
        else:
            result = None

        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)

    def multi_path_completion_handler(self, return_value: int) -> None:
        if return_value == NSFileHandlingPanelOKButton:
            result = [Path(url.path) for url in self.panel.URLs]
        else:
            result = None

        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)


class SaveFileDialog(FileDialog):
    def __init__(self, window, title, filename, initial_directory, file_types=None, on_result=None):
        super().__init__(
            window=window,
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=False,
            on_result=None,
        )

    def create_panel(self, multiselect):
        self.panel = NSSavePanel.alloc().init()


class OpenFileDialog(FileDialog):
    def __init__(self, window, title, initial_directory, file_types, multiselect, on_result=None):
        super().__init__(
            window=window,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            on_result=None,
        )

    def create_panel(self, multiselect):
        self.panel = NSOpenPanel.alloc().init()
        self.panel.allowsMultipleSelection = multiselect
        self.panel.canChooseDirectories = False
        self.panel.canCreateDirectories = False
        self.panel.canChooseFiles = True


class SelectFolderDialog(FileDialog):
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        super().__init__(
            window=window,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiselect=multiselect,
            on_result=None,
        )

    def create_panel(self, multiselect):
        self.panel = NSOpenPanel.alloc().init()
        self.panel.allowsMultipleSelection = multiselect
        self.panel.canChooseDirectories = True
        self.panel.canCreateDirectories = True
        self.panel.canChooseFiles = False
        self.panel.resolvesAliases = True
