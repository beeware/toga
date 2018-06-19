from travertino.layout import Viewport

from toga.command import Command as BaseCommand

from toga_cocoa import dialogs
from toga_cocoa.libs import *


def toolbar_identifier(cmd):
    return 'ToolbarItem-%s' % id(cmd)


class CocoaViewport:
    def __init__(self, view):
        self.view = view
        self.dpi = 96  # FIXME This is almost certainly wrong...

    @property
    def width(self):
        return self.view.frame.size.width

    @property
    def height(self):
        return self.view.frame.size.height


class WindowDelegate(NSObject):
    @objc_method
    def windowWillClose_(self, notification) -> None:
        self.interface.on_close()

    @objc_method
    def windowDidResize_(self, notification) -> None:
        if self.interface.content:
            # print()
            # print("Window resize", (notification.object.contentView.frame.size.width, notification.object.contentView.frame.size.height))
            if notification.object.contentView.frame.size.width > 0.0 and notification.object.contentView.frame.size.height > 0.0:
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
        _item = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        try:
            item = self.interface._impl._toolbar_items[identifier]
            impl = item.bind(self.interface.factory)
            if item.label:
                _item.setLabel(item.label)
                _item.setPaletteLabel(item.label)
            if item.tooltip:
                _item.setToolTip(item.tooltip)
            if impl.icon:
                _item.setImage(impl.icon.bind(self.interface.factory).native)

            item._widgets.append(_item)

            _item.setTarget_(self)
            _item.setAction_(SEL('onToolbarButtonPress:'))
        except KeyError:
            pass
        return _item

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        "Confirm if the toolbar item should be enabled"
        return self.interface._impl._toolbar_items[item.itemIdentifier].enabled

    ######################################################################
    # Toolbar button press delegate methods
    ######################################################################

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        "Invoke the action tied to the toolbar button"
        item = self.interface._impl._toolbar_items[obj.itemIdentifier]
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
        widget.viewport = CocoaViewport(widget.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        # Enforce a minimum size based on the content
        self._min_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            widget.native, NSLayoutAttributeRight,
            NSLayoutRelationGreaterThanOrEqual if self.interface.resizeable else NSLayoutRelationEqual,
            widget.native, NSLayoutAttributeLeft,
            1.0, 100
        )
        widget.native.addConstraint(self._min_width_constraint)

        self._min_height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            widget.native, NSLayoutAttributeBottom,
            NSLayoutRelationGreaterThanOrEqual if self.interface.resizeable else NSLayoutRelationEqual,
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
        self.native.setFrame(frame, display=True, animate=False)

    def set_app(self, app):
        pass

    def show(self):
        self.native.makeKeyAndOrderFront(None)

        # Render of the content with a 0 sized viewport; this will
        # establish the minimum possible content size. Use that to enforce
        # a minimum window size.
        self.interface.content.style.layout(self.interface.content, Viewport(0, 0))
        self._min_width_constraint.constant = self.interface.content.layout.width
        self._min_height_constraint.constant = self.interface.content.layout.height

        # Refresh with the actual viewport to do the proper rendering.
        self.interface.content.refresh()

    def on_close(self):
        pass

    def close(self):
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
