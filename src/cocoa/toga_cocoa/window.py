from toga.interface.window import Window as WindowInterface
from toga.interface.command import Command as BaseCommand, GROUP_BREAK, SECTION_BREAK

from .container import Container
from .command import Command
from .libs import *
from .utils import process_callback
from . import dialogs


def toolbar_identifier(cmd):
    return 'ToolbarItem-%s' % id(cmd)


class WindowDelegate(NSObject):
    @objc_method
    def windowWillClose_(self, notification) -> None:
        self._interface.on_close()

    @objc_method
    def windowDidResize_(self, notification) -> None:
        if self._interface.content:
            # print()
            # print("Window resize", (notification.object.contentView.frame.size.width, notification.object.contentView.frame.size.height))
            if notification.object.contentView.frame.size.width > 0.0 and notification.object.contentView.frame.size.height > 0.0:
                # Force a re-layout of widgets
                self._interface.content._update_layout(
                    width=notification.object.contentView.frame.size.width,
                    height=notification.object.contentView.frame.size.height
                )

    ######################################################################
    # Toolbar delegate methods
    ######################################################################

    @objc_method
    def toolbarAllowedItemIdentifiers_(self, toolbar):
        "Determine the list of available toolbar items"
        # This method is required by the Cocoa API, but isn't actually invoked,
        # because customizable toolbars are no longer a thing.
        allowed = NSMutableArray.alloc().init()
        for item in self._interface.toolbar:
            if isinstance(item, Command):
                default.addObject(toolbar_identifier(item))
        return allowed

    @objc_method
    def toolbarDefaultItemIdentifiers_(self, toolbar):
        "Determine the list of toolbar items that will display by default"
        default = NSMutableArray.alloc().init()
        for item in self._interface.toolbar:
            if isinstance(item, Command):
                default.addObject(toolbar_identifier(item))
        return default

    @objc_method
    def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(self, toolbar, identifier, insert: bool):
        "Create the requested toolbar button"
        item = self._interface._toolbar_items[identifier]

        _item = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        if item.label:
            _item.setLabel_(item.label)
            _item.setPaletteLabel_(item.label)
        if item.tooltip:
            _item.setToolTip_(item.tooltip)
        if item.icon:
            _item.setImage_(item.icon._impl)

        item._widgets.append(_item)

        _item.setTarget_(self)
        _item.setAction_(SEL('onToolbarButtonPress:'))

        return _item

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        "Confirm if the toolbar item should be enabled"
        return self._interface._toolbar_items[item.itemIdentifier].enabled

    ######################################################################
    # Toolbar button press delegate methods
    ######################################################################

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        "Invoke the action tied to the toolbar button"
        item = self._interface._toolbar_items[obj.itemIdentifier]
        process_callback(item.action(obj))


class Window(WindowInterface):
    _IMPL_CLASS = NSWindow
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=title, position=position, size=size, resizeable=resizeable, closeable=closeable, minimizable=minimizable)
        self._create()

    def create(self):
        # OSX origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        screen = NSScreen.mainScreen().visibleFrame
        position = NSMakeRect(
            screen.origin.x + self.position[0],
            screen.size.height + screen.origin.y - self.position[1] - self._size[1],
            self._size[0],
            self._size[1]
        )

        mask = NSTitledWindowMask
        if self.closeable:
            mask |= NSClosableWindowMask

        if self.resizeable:
            mask |= NSResizableWindowMask

        if self.minimizable:
            mask |= NSMiniaturizableWindowMask

        self._impl = self._IMPL_CLASS.alloc().initWithContentRect_styleMask_backing_defer_(
            position,
            mask,
            NSBackingStoreBuffered,
            False
        )
        self._impl.setFrame_display_animate_(position, True, False)

        self._delegate = WindowDelegate.alloc().init()
        self._delegate._interface = self

        self._impl.setDelegate_(self._delegate)

    # Create a new frame on the same position with the new size doing
    #   a animation.
    def _set_size(self, size):
        if self._impl:
            screen = NSScreen.mainScreen().visibleFrame
            position = NSMakeRect(
                screen.origin.x + self.position[0],
                screen.size.height + screen.origin.y - self.position[1] - self._size[1],
                self._size[0],
                self._size[1]
            )
            self._impl.setFrame_display_animate_(position, True, True)

    def _create_toolbar(self):
        self._toolbar_items = {}
        for cmd in self.toolbar:
            if isinstance(cmd, BaseCommand):
                self._toolbar_items[toolbar_identifier(cmd)] = cmd

        self._toolbar_impl = NSToolbar.alloc().initWithIdentifier_('Toolbar-%s' % id(self))
        self._toolbar_impl.setDelegate_(self._delegate)
        self._impl.setToolbar_(self._toolbar_impl)

    def _set_content(self, widget):
        self._impl.setContentView_(self._container._impl)

        # Enforce a minimum size based on the content
        self._min_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._container._impl, NSLayoutAttributeRight,
            NSLayoutRelationGreaterThanOrEqual if self.resizeable else NSLayoutRelationEqual,
            self._container._impl, NSLayoutAttributeLeft,
            1.0, 0
        )
        self._container._impl.addConstraint_(self._min_width_constraint)

        self._min_height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._container._impl, NSLayoutAttributeBottom,
            NSLayoutRelationGreaterThanOrEqual if self.resizeable else NSLayoutRelationEqual,
            self._container._impl, NSLayoutAttributeTop,
            1.0, 0
        )
        self._container._impl.addConstraint_(self._min_height_constraint)

    def _set_title(self, title):
        self._impl.setTitle_(title)

    def show(self):
        self._impl.makeKeyAndOrderFront_(None)

        # The first render of the content will establish the
        # minimum possible content size; use that to enforce
        # a minimum window size.
        self._min_width_constraint.constant = self.content.layout.width
        self._min_height_constraint.constant = self.content.layout.height

        # Do the first layout render.
        self._container._update_layout(
            width=self._impl.contentView.frame.size.width,
            height=self._impl.contentView.frame.size.height,
        )

    def close(self):
        self._impl.close()
