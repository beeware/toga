from toga.command import Command as BaseCommand
from toga_cocoa import dialogs
from toga_cocoa.libs import (
    SEL,
    NSBackingStoreBuffered,
    NSClosableWindowMask,
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutConstraint,
    NSLayoutRelationGreaterThanOrEqual,
    NSMakeRect,
    NSMiniaturizableWindowMask,
    NSMutableArray,
    NSObject,
    NSResizableWindowMask,
    NSScreen,
    NSSize,
    NSTitledWindowMask,
    NSToolbar,
    NSToolbarItem,
    NSWindow,
    objc_method
)


def toolbar_identifier(cmd):
    return 'ToolbarItem-%s' % id(cmd)


class CocoaViewport:
    def __init__(self, view):
        self.view = view
        # macOS always renders at 96dpi. Scaling is handled
        # transparently at the level of the screen compositor.
        self.dpi = 96
        self.baseline_dpi = self.dpi

    @property
    def width(self):
        # If `view` is `None`, we'll treat this a 0x0 viewport.
        return 0 if self.view is None else self.view.frame.size.width

    @property
    def height(self):
        return 0 if self.view is None else self.view.frame.size.height


class WindowDelegate(NSObject):
    @objc_method
    def windowShouldClose_(self, notification) -> bool:
        return self.impl.cocoa_windowShouldClose()

    @objc_method
    def windowDidResize_(self, notification) -> None:
        if self.interface.content:
            # print()
            # print("Window resize", (
            #   notification.object.contentView.frame.size.width,
            #   notification.object.contentView.frame.size.height
            # ))
            if (
                notification.object.contentView.frame.size.width > 0.0
                and notification.object.contentView.frame.size.height > 0.0
            ):
                # Set the window to the new size
                self.interface.content.refresh()

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
            allowed.addObject_(toolbar_identifier(item))
        return allowed

    @objc_method
    def toolbarDefaultItemIdentifiers_(self, toolbar):
        "Determine the list of toolbar items that will display by default"
        default = NSMutableArray.alloc().init()
        for item in self.interface.toolbar:
            default.addObject_(toolbar_identifier(item))
        return default

    @objc_method
    def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(self, toolbar, identifier, insert: bool):
        "Create the requested toolbar button"
        native = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        try:
            item = self.interface._impl._toolbar_items[str(identifier)]
            if item.label:
                native.setLabel(item.label)
                native.setPaletteLabel(item.label)
            if item.tooltip:
                native.setToolTip(item.tooltip)
            if item.icon:
                native.setImage(item.icon._impl.native)

            item._impl.native.append(native)

            native.setTarget_(self)
            native.setAction_(SEL('onToolbarButtonPress:'))
        except KeyError:
            pass

        # Prevent the toolbar item from being deallocated when
        # no Python references remain
        native.retain()
        native.autorelease()
        return native

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        "Confirm if the toolbar item should be enabled"
        return self.interface._impl._toolbar_items[str(item.itemIdentifier)].enabled

    ######################################################################
    # Toolbar button press delegate methods
    ######################################################################

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        "Invoke the action tied to the toolbar button"
        item = self.interface._impl._toolbar_items[str(obj.itemIdentifier)]
        item.action(obj)


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        # OSX origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        screen = NSScreen.mainScreen.visibleFrame
        position = NSMakeRect(
            screen.origin.x + self.interface.position[0],
            screen.size.height + screen.origin.y - self.interface.position[1] - self.interface._size[1],
            self.interface._size[0],
            self.interface._size[1]
        )

        mask = NSTitledWindowMask
        if self.interface.closeable:
            mask |= NSClosableWindowMask

        if self.interface.resizeable:
            mask |= NSResizableWindowMask

        if self.interface.minimizable:
            mask |= NSMiniaturizableWindowMask

        self.native = NSWindow.alloc().initWithContentRect(
            position,
            styleMask=mask,
            backing=NSBackingStoreBuffered,
            defer=False
        )
        self.native.setFrame(position, display=True, animate=False)
        self.native.interface = self.interface
        self.native.impl = self

        self.delegate = WindowDelegate.alloc().init()
        self.delegate.interface = self.interface
        self.delegate.impl = self

        self.native.setDelegate_(self.delegate)

    def create_toolbar(self):
        self._toolbar_items = {}
        for cmd in self.interface.toolbar:
            if isinstance(cmd, BaseCommand):
                self._toolbar_items[toolbar_identifier(cmd)] = cmd

        self._toolbar_native = NSToolbar.alloc().initWithIdentifier_('Toolbar-%s' % id(self))
        self._toolbar_native.setDelegate_(self.delegate)

        self.native.setToolbar_(self._toolbar_native)

    def set_content(self, widget):
        # Set the window's view to the be the widget's native object.
        self.native.contentView = widget.native

        # Set the widget's viewport to be based on the window's content.
        widget.viewport = CocoaViewport(view=widget.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        # Enforce a minimum size based on the content size.
        # This is enforcing the *minimum* size; the window might actually be
        # bigger. If the window is resizable, using >= allows the window to
        # be dragged larged; if not resizable, it enforces the smallest
        # size that can be programmattically set on the window.
        self._min_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA: E501
            widget.native, NSLayoutAttributeRight,
            NSLayoutRelationGreaterThanOrEqual,
            widget.native, NSLayoutAttributeLeft,
            1.0, 100
        )
        widget.native.addConstraint(self._min_width_constraint)

        self._min_height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA: E501
            widget.native, NSLayoutAttributeBottom,
            NSLayoutRelationGreaterThanOrEqual,
            widget.native, NSLayoutAttributeTop,
            1.0, 100
        )
        widget.native.addConstraint(self._min_height_constraint)

    def set_title(self, title):
        self.native.title = title

    def set_position(self, position):
        pass

    def set_size(self, size):
        frame = self.native.frame
        frame.size = NSSize(self.interface._size[0], self.interface._size[1])
        self.native.setFrame(frame, display=True, animate=True)

    def set_app(self, app):
        pass

    def show(self):
        self.native.makeKeyAndOrderFront(None)

        # Render of the content with a 0 sized viewport; this will
        # establish the minimum possible content size. Use that to enforce
        # a minimum window size.
        self.interface.content.style.layout(
            self.interface.content,
            CocoaViewport(view=None),
        )
        self._min_width_constraint.constant = self.interface.content.layout.width
        self._min_height_constraint.constant = self.interface.content.layout.height

        # Refresh with the actual viewport to do the proper rendering.
        self.interface.content.refresh()

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')

    def set_on_close(self, handler):
        pass

    def cocoa_windowShouldClose(self):
        if self.interface.on_close:
            should_close = self.interface.on_close(self)
        else:
            should_close = True

        if should_close:
            self.interface.app.windows -= self.interface

        return should_close

    def close(self):
        # Close window directly here, don't use `NSWindow.performClose()`
        # because it won't work if the window does not have a close button.
        if self.cocoa_windowShouldClose():
            self.native.close()

    def info_dialog(self, title, message):
        return dialogs.info(self.interface, title, message)

    def question_dialog(self, title, message):
        return dialogs.question(self.interface, title, message)

    def confirm_dialog(self, title, message):
        return dialogs.confirm(self.interface, title, message)

    def error_dialog(self, title, message):
        return dialogs.error(self.interface, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        return dialogs.stack_trace(self.interface, title, message, content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types):
        return dialogs.save_file(self.interface, title, suggested_filename, file_types)

    def open_file_dialog(self, title, initial_directory, file_types, multiselect):
        return dialogs.open_file(self.interface, title, file_types, multiselect)

    def select_folder_dialog(self, title, initial_directory, multiselect):
        return dialogs.select_folder(self.interface, title, multiselect)
