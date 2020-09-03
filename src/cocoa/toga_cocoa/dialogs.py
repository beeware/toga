import asyncio
from .libs import (
    NSAlert,
    NSAlertFirstButtonReturn,
    NSAlertStyle,
    NSArray,
    NSBezelBorder,
    NSFileHandlingPanelOKButton,
    NSMakeRect,
    NSOpenPanel,
    NSSavePanel,
    NSScrollView,
    NSTextView
)


async def info(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon._impl.native
    alert.alertStyle = NSAlertStyle.Informational
    alert.messageText = title
    alert.informativeText = message

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        future.set_result(None)

    alert.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def question(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon._impl.native
    alert.alertStyle = NSAlertStyle.Informational
    alert.messageText = title
    alert.informativeText = message

    alert.addButtonWithTitle('Yes')
    alert.addButtonWithTitle('No')

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        future.set_result(r == NSAlertFirstButtonReturn)

    alert.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def confirm(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon._impl.native
    alert.alertStyle = NSAlertStyle.Warning
    alert.messageText = title
    alert.informativeText = message

    alert.addButtonWithTitle('OK')
    alert.addButtonWithTitle('Cancel')

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        future.set_result(r == NSAlertFirstButtonReturn)

    alert.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def error(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon._impl.native
    alert.alertStyle = NSAlertStyle.Critical
    alert.messageText = title
    alert.informativeText = message

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        future.set_result(None)

    alert.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def stack_trace(window, title, message, content, retry=False):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon._impl.native
    alert.alertStyle = NSAlertStyle.Critical
    alert.messageText = title
    alert.informativeText = message

    scroll = NSScrollView.alloc().initWithFrame(NSMakeRect(0, 0, 500, 200))
    scroll.hasVerticalScroller = True
    scroll.hasHorizontalScrolle = False
    scroll.autohidesScrollers = False
    scroll.borderType = NSBezelBorder

    trace = NSTextView.alloc().init()
    trace.insertText(content)
    trace.editable = False
    trace.werticallyResizable = True
    trace.horizontallyResizable = True

    scroll.documentView = trace
    alert.accessoryView = scroll

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        if retry:
            future.set_result(r == NSAlertFirstButtonReturn)
        else:
            future.set_result(None)

    if retry:
        alert.addButtonWithTitle('Retry')
        alert.addButtonWithTitle('Quit')

    alert.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def save_file(window, title, suggested_filename, file_types=None):
    panel = NSSavePanel.alloc().init()
    panel.title = title

    if file_types:
        arr = NSArray.alloc().init()
        for x in file_types:
            arr = arr.arrayByAddingObject_(x)
    else:
        arr = None

    panel.allowedFileTypes = arr
    panel.nameFieldStringValue = suggested_filename

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        if r == NSFileHandlingPanelOKButton:
            future.set_result(panel.URL.path)
        else:
            future.set_result(None)

    panel.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def open_file(window, title, file_types, multiselect):
    """Cocoa open file dialog implementation.

    We restrict the panel invocation to only choose files. We also allow
    creating directories but not selecting directories.

    Args:
        window: The window this dialog belongs to.
        title: Title of the modal.
        file_types: Ignored for now.
        multiselect: Flag to allow multiple file selection.
    Returns:
        (list) A list of file paths (may be empty).
    """

    # Initialize and configure the panel.
    panel = NSOpenPanel.alloc().init()
    panel.title = title
    panel.allowedFileTypes = file_types
    panel.allowsMultipleSelection = multiselect
    panel.canChooseDirectories = False
    panel.canCreateDirectories = False
    panel.canChooseFiles = True

    # Show modal and return file path on success.
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:
        if r == NSFileHandlingPanelOKButton:
            if multiselect:
                paths = [str(url.path) for url in panel.URLs]
            else:
                paths = [str(panel.URL.path)]
        else:
            paths = []

        future.set_result(paths)

    panel.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future


async def select_folder(window, title, multiselect):
    """Cocoa select folder dialog implementation.

    Args:
        window: Window dialog belongs to.
        title: Title of the dialog.
        multiselect: Flag to allow multiple folder selection.
    Returns:
        (list) A list of folder paths (may be empty).
    """
    panel = NSOpenPanel.alloc().init()
    panel.title = title

    panel.canChooseFiles = False
    panel.canChooseDirectories = True
    panel.resolvesAliases = True
    panel.allowsMultipleSelection = multiselect

    # Show modal and return file path on success.
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def completion_handler(r: int) -> None:

        # Ensure regardless of the result, return types remain the same so as to not
        # require type checking logic in user code.
        # Convert types from 'ObjCStrInstance' to 'str'.

        if r == NSFileHandlingPanelOKButton:
            if multiselect:
                paths = [str(url.path) for url in panel.URLs]
            else:
                paths = [str(panel.URL.path)]
        else:
            paths = []

        future.set_result(paths)

    panel.beginSheetModalForWindow(window._impl.native, completionHandler=completion_handler)

    return await future
