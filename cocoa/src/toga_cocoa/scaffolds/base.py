from rubicon.objc import SEL, NSObject, objc_method, objc_property

from toga.command import Command, Separator
from toga_cocoa.container import ControlledContainer
from toga_cocoa.libs import NSMutableArray, NSToolbar, NSToolbarItem


def toolbar_identifier(cmd):
    return f"Toolbar-{type(cmd).__name__}-{id(cmd)}"


class ToolbarDelegate(NSObject):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def toolbarAllowedItemIdentifiers_(self, toolbar):  # pragma: no cover
        """Determine the list of available toolbar items."""
        allowed = NSMutableArray.alloc().init()
        for item in self.impl.toolbar_commands:
            allowed.addObject_(toolbar_identifier(item))
        return allowed

    @objc_method
    def toolbarDefaultItemIdentifiers_(self, toolbar):
        """Determine the list of toolbar items that will display by default."""
        default = NSMutableArray.alloc().init()
        prev_group = None
        for item in self.impl.toolbar_commands:
            if (
                prev_group is not None
                and item.group != prev_group
                and not isinstance(item, Separator)
            ):
                default.addObject_(toolbar_identifier(prev_group))
            default.addObject_(toolbar_identifier(item))
            prev_group = item.group

        return default

    @objc_method
    def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(
        self,
        toolbar,
        identifier,
        insert: bool,
    ):
        """Create the requested toolbar button."""
        native = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        try:
            item = self.impl._toolbar_items[str(identifier)]
            native.setLabel(item.text)
            native.setPaletteLabel(item.text)
            if item.tooltip:
                native.setToolTip(item.tooltip)
            if item.icon:
                native.setImage(item.icon._impl.native)

            item._impl.native.add(native)

            native.setTarget_(self)
            native.setAction_(SEL("onToolbarButtonPress:"))
        except KeyError:  # Separator items
            pass

        return native

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        """Confirm if the toolbar item should be enabled."""
        try:
            return self.impl._toolbar_items[str(item.itemIdentifier)].enabled
        except KeyError:  # pragma: nocover
            return False

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        """Invoke the action tied to the toolbar button."""
        item = self.impl._toolbar_items[str(obj.itemIdentifier)]
        item.action()


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self.container = ControlledContainer(on_refresh=self.content_refreshed)
        self.root_controller = self.container.controller
        self._toolbar_items = {}
        self._toolbar_commands = []
        self.native_toolbar = None
        self.toolbar_delegate = ToolbarDelegate.alloc().init()
        self.toolbar_delegate.impl = self
        self.toolbar_delegate.interface = self.interface

    def __del_(self):
        self.purge_toolbar()

    @property
    def current_container(self):
        return self.container

    def set_content(self, widget):
        self.container.content = widget

    @property
    def title(self):
        return self.container.controller.title

    @title.setter
    def title(self, value):
        self.container.controller.title = value

    def refresh(self):
        if self.container.content:
            self.container.content.interface.refresh()

    @property
    def toolbar_commands(self):
        return self._toolbar_commands

    # def notify_toolbar_change(self):
    #     window = self.interface.window
    #     if window is not None and getattr(window, "_impl", None) is not None:
    #         window._impl.update_toolbar(self)

    def create_toolbar(self):
        window = self.interface.window
        self.purge_toolbar()

        # Shouldn't happen in normal operations, but just in case
        if window is None:  # pragma: no cover
            self.native_toolbar = None
            self._toolbar_commands = []
            return

        self._toolbar_commands = []
        if hasattr(window, "toolbar"):
            self._toolbar_commands.extend(window.toolbar)

        self._toolbar_items = {}
        for cmd in self._toolbar_commands:
            if isinstance(cmd, Command):
                self._toolbar_items[toolbar_identifier(cmd)] = cmd

        if self._toolbar_commands:
            self.native_toolbar = NSToolbar.alloc().initWithIdentifier(
                f"Toolbar-{id(self)}"
            )
            self.native_toolbar.setDelegate(self.toolbar_delegate)
        else:
            self.native_toolbar = None

        if window.content:
            window.content.refresh()

    def purge_toolbar(self):
        window = self.interface.window

        # Defensive measure
        if window is None:  # pragma: no cover
            return

        while self._toolbar_items:
            dead_items = []
            _, cmd = self._toolbar_items.popitem()
            # Only purge items associated with the current scaffold's
            # toolbar delegate.  This ensures proper cleanup.
            for item_native in cmd._impl.native:
                if (
                    isinstance(item_native, NSToolbarItem)
                    and item_native.target == self.toolbar_delegate
                ):
                    dead_items.append(item_native)

            for item_native in dead_items:
                cmd._impl.native.remove(item_native)

    def content_refreshed(self, container):
        # Apply the minimum size.  This will autoresize the window if needed.
        self.container.min_width = self.interface.content.layout.min_width
        self.container.min_height = self.interface.content.layout.min_height
