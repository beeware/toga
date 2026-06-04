from ctypes import c_void_p

from rubicon.objc import SEL, objc_method, objc_property
from rubicon.objc.runtime import send_super
from travertino.size import at_least

from toga_cocoa.libs import (
    NSFocusRingType,
    NSImage,
    NSMenu,
    NSMenuItem,
    NSTableColumn,
    NSTableRowActionEdge,
    NSTableView,
    NSTableViewColumnAutoresizingStyle,
    NSTableViewRowAction,
    NSTableViewRowActionStyle,
)
from toga_cocoa.widgets.base import Widget
from toga_cocoa.widgets.internal.cells import TogaDetailedView
from toga_cocoa.widgets.internal.refresh import RefreshableScrollView

REFRESH_IMAGE = NSImage.imageWithSystemSymbolName_accessibilityDescription_(
    "arrow.clockwise", "refresh"
)


class TogaList(NSTableView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def didCloseMenu_withEvent_(self, menu, event) -> None:
        # When the menu closes, drop the reference to the menu object.
        self.impl._popup = None

    @objc_method
    def menu(self):
        if (
            self.clickedRow == -1 or self.clickedColumn == -1
        ):  # Somehow this happens in VoiceOver
            return NSMenu(send_super(__class__, self, "menu"))
        # Create a popup menu to display the possible actions.
        popup = NSMenu.alloc().initWithTitle("popup")
        if self.impl.primary_action_enabled:
            primary_action_item = popup.addItemWithTitle(
                self.interface._primary_action,
                action=SEL("primaryActionOnRow:"),
                keyEquivalent="",
            )
            primary_action_item.tag = self.clickedRow

        if self.impl.secondary_action_enabled:
            secondary_action_item = popup.addItemWithTitle(
                self.interface._secondary_action,
                action=SEL("secondaryActionOnRow:"),
                keyEquivalent="",
            )
            secondary_action_item.tag = self.clickedRow
        if self.impl.refresh_enabled:
            popup.addItem(NSMenuItem.separatorItem())
            refresh_action_item = popup.addItemWithTitle(
                "Refresh",
                action=SEL("onInterfaceRefresh:"),
                keyEquivalent="",
            )
            refresh_action_item.image = REFRESH_IMAGE
            refresh_action_item.tag = self.clickedRow

        self.impl._popup = popup
        return popup

    @objc_method
    def onInterfaceRefresh_(self, menuitem):
        self.interface.on_refresh()

    @objc_method
    def primaryActionOnRow_(self, menuitem):
        row = self.interface.data[menuitem.tag]
        self.interface.on_primary_action(row=row)

    @objc_method
    def secondaryActionOnRow_(self, menuitem):
        row = self.interface.data[menuitem.tag]
        self.interface.on_secondary_action(row=row)

    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.interface.data) if self.interface.data else 0

    @objc_method
    def tableView_rowActionsForRow_edge_(self, table, row: int, edge: int):
        # This API needs a block, not a selector, hence the redefinition of a handler
        # instead of using primaryActionOnRow: and secondaryActionOnRow:.
        def handler(action: c_void_p, index: int) -> None:
            row = self.interface.data[index]
            if edge == NSTableRowActionEdge.Trailing:
                self.interface.on_primary_action(row=row)
            elif edge == NSTableRowActionEdge.Leading:
                self.interface.on_secondary_action(row=row)

        if edge == NSTableRowActionEdge.Trailing and self.impl.primary_action_enabled:
            style = (
                NSTableViewRowActionStyle.Default
                if self.interface._primary_action not in self.impl.DESTRUCTIVE_ACTIONS
                else NSTableViewRowActionStyle.Destructive
            )
            return [
                NSTableViewRowAction.rowActionWithStyle_title_handler_(
                    style, self.interface._primary_action, handler
                )
            ]
        if edge == NSTableRowActionEdge.Leading and self.impl.secondary_action_enabled:
            style = (
                NSTableViewRowActionStyle.Default
                if self.interface._secondary_action not in self.impl.DESTRUCTIVE_ACTIONS
                else NSTableViewRowActionStyle.Destructive
            )
            return [
                NSTableViewRowAction.rowActionWithStyle_title_handler_(
                    style, self.interface._secondary_action, handler
                )
            ]
        return []

    @objc_method
    def tableView_viewForTableColumn_row_(self, table, column, row: int):
        identifier = "DetailedCell"

        view = table.makeViewWithIdentifier_owner_(
            identifier,
            self,
        )

        if view is None:
            view = TogaDetailedView.alloc().init()
            view.setup()
            view.setIdentifier(identifier)

        value = self.interface.data[row]
        try:
            title = getattr(value, self.interface.accessors[0])
        except AttributeError:
            title = self.interface.missing_value

        try:
            subtitle = getattr(value, self.interface.accessors[1])
        except AttributeError:
            subtitle = self.interface.missing_value

        try:
            icon = getattr(value, self.interface.accessors[2])._impl.native
        except AttributeError:
            icon = None

        view.setTitle(str(title))
        view.setSubtitle(str(subtitle))
        view.setIcon(icon)

        return view

    # TableDelegate methods
    @objc_method
    def tableView_heightOfRow_(self, table, row: int) -> float:
        return 48.0

    @objc_method
    def selectionShouldChangeInTableView_(self, table) -> bool:
        # Explicitly allow selection on the table.
        # TODO: return False to disable selection.
        return True

    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        self.interface.on_select()


class DetailedList(Widget):
    DESTRUCTIVE_ACTIONS = {"Delete", "Remove"}

    def create(self):
        # Create a List, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.

        # Create the List widget
        self.native_detailedlist = TogaList.alloc().init()
        self.native_detailedlist.interface = self.interface
        self.native_detailedlist.impl = self
        self.native_detailedlist.columnAutoresizingStyle = (
            NSTableViewColumnAutoresizingStyle.Uniform
        )
        self.native_detailedlist.focusRingType = NSFocusRingType.None_
        self.native_detailedlist.allowsMultipleSelection = False

        # Disable all actions by default.
        self.primary_action_enabled = False
        self.secondary_action_enabled = False
        self.refresh_enabled = False

        self.native = RefreshableScrollView.alloc().initWithDocument(
            self.native_detailedlist
        )
        self.native.interface = self.interface
        self.native.impl = self

        # Create the column for the detailed list
        column = NSTableColumn.alloc().initWithIdentifier("data")
        self.native_detailedlist.addTableColumn(column)
        self.columns = [column]

        # Hide the column header.
        self.native_detailedlist.headerView = None

        self.native_detailedlist.delegate = self.native_detailedlist
        self.native_detailedlist.dataSource = self.native_detailedlist

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.native_detailedlist.reloadData()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        self.native_detailedlist.reloadData()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        import warnings

        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        self.native_detailedlist.reloadData()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        self.native_detailedlist.reloadData()

        # After deletion, the selection changes, but Cocoa doesn't send
        # a tableViewSelectionDidChange: message.
        self.interface.on_select()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        self.native_detailedlist.reloadData()

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled
        self.native.setRefreshEnabled(enabled)

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def after_on_refresh(self, widget, result):
        self.native.finishedLoading()

    def get_selection(self):
        index = self.native_detailedlist.selectedRow
        if index == -1:
            return None
        else:
            return index

    def scroll_to_row(self, row):
        self.native_detailedlist.scrollRowToVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
