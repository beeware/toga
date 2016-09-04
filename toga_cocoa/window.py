from .libs import *
from .utils import process_callback


class WindowDelegate(NSObject):
    @objc_method
    def windowWillClose_(self, notification) -> None:
        self.interface.on_close()

    # Ideally, we'd use this method, not windowDidResize_, as it
    # allows you to enforce a minimum size for the window. Unfortunately,
    # ctypes can't return a structure from a callback.
    # @objc_method
    # def windowWillResize_toSize_(self, window, size: NSSize) -> NSSize:
    #     return size

    @objc_method
    def windowDidResize_(self, notification) -> None:
        if self.interface.content:
            # print()
            # print("Window resize", (notification.object.contentView.frame.size.width, notification.object.contentView.frame.size.height))
            if notification.object.contentView.frame.size.width > 0.0 and notification.object.contentView.frame.size.height > 0.0:
                # Force a re-layout of widgets
                self.interface.content._update_layout(
                    width=notification.object.contentView.frame.size.width,
                    height=notification.object.contentView.frame.size.height
                )
                # Force a redraw with the new widget locations
                self.interface.content._impl.setNeedsDisplay_(True)

    ######################################################################
    # Toolbar delegate methods
    ######################################################################

    @objc_method
    def toolbarAllowedItemIdentifiers_(self, toolbar):
        "Determine the list of available toolbar items"
        # This method is required by the Cocoa API, but isn't actually invoked,
        # because customizable toolbars are no longer a thing.
        allowed = NSMutableArray.alloc().init()
        for item in self.interface.toolbar:
            allowed.addObject_(item.toolbar_identifier)
        return allowed

    @objc_method
    def toolbarDefaultItemIdentifiers_(self, toolbar):
        "Determine the list of toolbar items that will display by default"
        default = NSMutableArray.alloc().init()
        for item in self.interface.toolbar:
            default.addObject_(item.toolbar_identifier)
        return default

    @objc_method
    def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(self, toolbar, identifier, insert: bool):
        "Create the requested toolbar button"
        item = self.interface._toolbar_items[identifier]
        _item = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        if item.label:
            _item.setLabel_(item.label)
            _item.setPaletteLabel_(item.label)
        if item.tooltip:
            _item.setToolTip_(item.tooltip)
        if item.icon:
            _item.setImage_(item.icon._impl)

        _item.setTarget_(self)
        _item.setAction_(get_selector('onToolbarButtonPress:'))

        return _item

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        "Confirm if the toolbar item should be enabled"
        return self.interface._toolbar_items[item.itemIdentifier].enabled

    ######################################################################
    # Toolbar button press delegate methods
    ######################################################################

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        "Invoke the action tied to the toolbar button"
        item = self.interface._toolbar_items[obj.itemIdentifier]
        process_callback(item.action(obj))


class Window(object):
    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True):
        self._impl = None
        self._app = None
        self._toolbar = None
        self._content = None

        self.position = position
        self.size = size

        self.resizeable = resizeable
        self.closeable = closeable
        self.minimizable = minimizable

        self.startup()

        self.title = title
        self.toolbar = toolbar

    def startup(self):
        # OSX origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        screen = NSScreen.mainScreen().visibleFrame
        position = NSMakeRect(
            screen.origin.x + self.position[0],
            screen.size.height + screen.origin.y - self.position[1] - self.size[1],
            self.size[0],
            self.size[1]
        )

        mask = NSTitledWindowMask
        if self.closeable:
            mask |= NSClosableWindowMask

        if self.resizeable:
            mask |= NSResizableWindowMask

        if self.minimizable:
            mask |= NSMiniaturizableWindowMask

        self._impl = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            position,
            mask,
            NSBackingStoreBuffered,
            False
        )
        self._impl.setFrame_display_animate_(position, True, False)

        self._delegate = WindowDelegate.alloc().init()
        self._delegate.interface = self

        self._impl.setDelegate_(self._delegate)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, toolbar):
        self._toolbar = toolbar
        if self._toolbar:
            self._toolbar_items = dict((item.toolbar_identifier, item) for item in self._toolbar)
            self._toolbar_impl = NSToolbar.alloc().initWithIdentifier_('Toolbar-%s' % id(self))
            self._toolbar_impl.setDelegate_(self._delegate)
            self._impl.setToolbar_(self._toolbar_impl)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self

        # Assign the widget to the same app as the window.
        self.content.app = self.app

        self._impl.setContentView_(self._content._impl)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        if self._title is not None:
            self._impl.setTitle_(self._title)
        else:
            self._impl.setTitle_('Toga')

    def show(self):
        self._impl.makeKeyAndOrderFront_(None)

        # Do the first layout render.
        self.content._update_layout(
            width=self.content._impl.frame.size.width,
            height=self.content._impl.frame.size.height
        )

    def close(self):
        self._impl.close()

    def on_close(self):
        pass
