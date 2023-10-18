from toga.command import Command as BaseCommand
from toga_cocoa.container import Container
from toga_cocoa.libs import (
    SEL,
    NSBackingStoreBuffered,
    NSMakeRect,
    NSMutableArray,
    NSPoint,
    NSScreen,
    NSSize,
    NSToolbar,
    NSToolbarItem,
    NSWindow,
    NSWindowStyleMask,
    objc_method,
    objc_property,
)


def toolbar_identifier(cmd):
    return "ToolbarItem-%s" % id(cmd)


class TogaWindow(NSWindow):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def windowShouldClose_(self, notification) -> bool:
        return self.impl.cocoa_windowShouldClose()

    @objc_method
    def windowDidResize_(self, notification) -> None:
        if self.interface.content:
            # Set the window to the new size
            self.interface.content.refresh()

    ######################################################################
    # Toolbar delegate methods
    ######################################################################

    @objc_method
    def toolbarAllowedItemIdentifiers_(self, toolbar):
        """Determine the list of available toolbar items."""
        # This method is required by the Cocoa API, but isn't actually invoked,
        # because customizable toolbars are no longer a thing.
        allowed = NSMutableArray.alloc().init()
        for item in self.interface.toolbar:
            allowed.addObject_(toolbar_identifier(item))
        return allowed

    @objc_method
    def toolbarDefaultItemIdentifiers_(self, toolbar):
        """Determine the list of toolbar items that will display by default."""
        default = NSMutableArray.alloc().init()
        for item in self.interface.toolbar:
            default.addObject_(toolbar_identifier(item))
        return default

    @objc_method
    def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(
        self, toolbar, identifier, insert: bool
    ):
        """Create the requested toolbar button."""
        native = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        try:
            item = self.impl._toolbar_items[str(identifier)]
            if item.text:
                native.setLabel(item.text)
                native.setPaletteLabel(item.text)
            if item.tooltip:
                native.setToolTip(item.tooltip)
            if item.icon:
                native.setImage(item.icon._impl.native)

            item._impl.native.append(native)

            native.setTarget_(self)
            native.setAction_(SEL("onToolbarButtonPress:"))
        except KeyError:
            pass

        # Prevent the toolbar item from being deallocated when
        # no Python references remain
        native.retain()
        native.autorelease()
        return native

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        """Confirm if the toolbar item should be enabled."""
        return self.impl._toolbar_items[str(item.itemIdentifier)].enabled

    ######################################################################
    # Toolbar button press delegate methods
    ######################################################################

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        """Invoke the action tied to the toolbar button."""
        item = self.impl._toolbar_items[str(obj.itemIdentifier)]
        item.action(obj)


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        mask = NSWindowStyleMask.Titled
        if self.interface.closable:
            mask |= NSWindowStyleMask.Closable

        if self.interface.resizable:
            mask |= NSWindowStyleMask.Resizable

        if self.interface.minimizable:
            mask |= NSWindowStyleMask.Miniaturizable

        # Create the window with a default frame;
        # we'll update size and position later.
        self.native = TogaWindow.alloc().initWithContentRect(
            NSMakeRect(0, 0, 0, 0),
            styleMask=mask,
            backing=NSBackingStoreBuffered,
            defer=False,
        )
        self.native.interface = self.interface
        self.native.impl = self

        # Cocoa releases windows when they are closed; this causes havoc with
        # Toga's widget cleanup because the ObjC runtime thinks there's no
        # references to the object left. Add an explicit reference to the window.
        self.native.retain()

        self.set_title(title)
        self.set_size(size)
        self.set_position(position)

        self.native.delegate = self.native

        self.container = Container(on_refresh=self.content_refreshed)
        self.native.contentView = self.container.native

    def __del__(self):
        self.native.release()

    def create_toolbar(self):
        self._toolbar_items = {}
        for cmd in self.interface.toolbar:
            if isinstance(cmd, BaseCommand):
                self._toolbar_items[toolbar_identifier(cmd)] = cmd

        self._toolbar_native = NSToolbar.alloc().initWithIdentifier(
            "Toolbar-%s" % id(self)
        )
        self._toolbar_native.setDelegate(self.native)

        self.native.setToolbar(self._toolbar_native)

    def set_content(self, widget):
        # Set the content of the window's container
        self.container.content = widget

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height

        # If the minimum layout is bigger than the current window,
        # increase the size of the window.
        frame = self.native.frame
        if frame.size.width < min_width and frame.size.height < min_height:
            self.set_size((min_width, min_height))
        elif frame.size.width < min_width:
            self.set_size((min_width, frame.size.height))
        elif frame.size.height < min_height:
            self.set_size((frame.size.width, min_height))

        self.container.min_width = min_width
        self.container.min_height = min_height

    def get_title(self):
        return str(self.native.title)

    def set_title(self, title):
        self.native.title = title

    def get_position(self):
        # The "primary" screen has index 0 and origin (0, 0).
        primary_screen = NSScreen.screens[0].frame
        window_frame = self.native.frame

        # macOS origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        return (
            window_frame.origin.x,
            primary_screen.size.height
            - (window_frame.origin.y + window_frame.size.height),
        )

    def set_position(self, position):
        # The "primary" screen has index 0 and origin (0, 0).
        primary_screen = NSScreen.screens[0].frame

        # macOS origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        x = position[0]
        y = primary_screen.size.height - position[1]

        self.native.setFrameTopLeftPoint(NSPoint(x, y))

    def get_size(self):
        frame = self.native.frame
        return frame.size.width, frame.size.height

    def set_size(self, size):
        frame = self.native.frame
        frame.size = NSSize(size[0], size[1])
        self.native.setFrame(frame, display=True, animate=True)

    def set_app(self, app):
        pass

    def show(self):
        self.native.makeKeyAndOrderFront(None)

    def hide(self):
        self.native.orderOut(self.native)

    def get_visible(self):
        return bool(self.native.isVisible)

    def set_full_screen(self, is_full_screen):
        current_state = bool(self.native.styleMask & NSWindowStyleMask.FullScreen)
        if is_full_screen != current_state:
            self.native.toggleFullScreen(self.native)

    def cocoa_windowShouldClose(self):
        # The on_close handler has a cleanup method that will enforce
        # the close if the on_close handler requests it; this initial
        # "should close" request can always return False.
        self.interface.on_close(None)
        return False

    def close(self):
        self.native.close()
