from rubicon.objc import objc_method, at, send_super
from travertino.size import at_least

from toga_cocoa.libs import (
    NSBezelBorder,
    NSOutlineView,
    NSScrollView,
    NSTableColumn,
    NSTableViewColumnAutoresizingStyle,
    NSIndexSet,
    NSTableViewAnimation,
    CGRectMake,
    # NSSortDescriptor,
)
import toga
from toga.keys import Key
from toga_cocoa.keys import toga_key
from toga_cocoa.widgets.base import Widget
from toga_cocoa.widgets.internal.data import TogaData
from toga_cocoa.widgets.internal.cells import TogaIconView


class TogaTree(NSOutlineView):
    # OutlineViewDataSource methods
    @objc_method
    def outlineView_child_ofItem_(self, tree, child: int, item):
        # Get the object representing the row
        if item is None:
            node = self.interface.data[child]
        else:
            node = item.attrs['node'][child]

        # Get the Cocoa implementation for the row. If an _impl
        # doesn't exist, create a data object for it, and
        # populate it with initial values for each column.
        try:
            node_impl = node._impl
        except AttributeError:
            node_impl = TogaData.alloc().init()
            node_impl.attrs = {'node': node}
            node._impl = node_impl

        return node_impl

    @objc_method
    def outlineView_isItemExpandable_(self, tree, item) -> bool:
        try:
            return item.attrs['node'].can_have_children()
        except AttributeError:
            return False

    @objc_method
    def outlineView_numberOfChildrenOfItem_(self, tree, item) -> int:
        if item is None:
            # How many root elements are there?
            # If we're starting up, the source may not exist yet.
            if self.interface.data is not None:
                return len(self.interface.data)
            else:
                return 0
        else:
            # How many children does this node have?
            return len(item.attrs['node'])

    @objc_method
    def outlineView_viewForTableColumn_item_(self, tree, column, item):
        col_identifier = self._impl.column_identifiers[id(column.identifier)]

        try:
            value = getattr(item.attrs['node'], col_identifier)

            # if the value is a widget itself, just draw the widget!
            if isinstance(value, toga.Widget):
                return value._impl.native

            # Allow for an (icon, value) tuple as the simple case
            # for encoding an icon in a table cell. Otherwise, look
            # for an icon attribute.
            elif isinstance(value, tuple):
                icon_iface, value = value
            else:
                try:
                    icon_iface = value.icon
                except AttributeError:
                    icon_iface = None
        except AttributeError:
            # If the node doesn't have a property with the
            # accessor name, assume an empty string value.
            value = ''
            icon_iface = None

        # If the value has an icon, get the _impl.
        # Icons are deferred resources, so we provide the factory.
        if icon_iface:
            icon = icon_iface.bind(self.interface.factory)
        else:
            icon = None

        # creates a NSTableCellView from interface-builder template (does not exist)
        # or reuses an existing view which is currently not needed for painting
        # returns None (nil) if both fails
        identifier = at('CellView_{}'.format(self.interface.id))
        tcv = self.makeViewWithIdentifier(identifier, owner=self)

        if not tcv:  # there is no existing view to reuse so create a new one
            tcv = TogaIconView.alloc().initWithFrame_(CGRectMake(0, 0, column.width, 16))
            tcv.identifier = identifier

        tcv.setText(str(value))
        if icon:
            tcv.setImage(icon.native)
        else:
            tcv.setImage(None)

        return tcv

    @objc_method
    def outlineView_heightOfRowByItem_(self, tree, item) -> float:

        min_row_size = 18

        if item is self:
            return min_row_size

        # get all views in column
        views = [self.outlineView_viewForTableColumn_item_(tree, col, item) for col in self.tableColumns]

        max_widget_size = max(view.intrinsicContentSize().height for view in views)
        return max(min_row_size, max_widget_size)

    # @objc_method
    # def outlineView_sortDescriptorsDidChange_(self, tableView, oldDescriptors) -> None:
    #
    #     for descriptor in self.sortDescriptors[::-1]:
    #         accessor = descriptor.key
    #         reverse = descriptor.ascending == 1
    #         key = self.interface._sort_keys[str(accessor)]
    #         try:
    #             self.interface.data.sort(str(accessor), reverse=reverse, key=key)
    #         except AttributeError:
    #             pass
    #         else:
    #             self.reloadData()

    @objc_method
    def keyDown_(self, event) -> None:
        # any time this table is in focus and a key is pressed, this method will be called
        if toga_key(event) == {'key': Key.A, 'modifiers': {Key.MOD_1}}:
            if self.interface.multiple_select:
                self.selectAll(self)
        else:
            # forawrd call to super
            send_super(__class__, self, 'keyDown:', event)

    # OutlineViewDelegate methods
    @objc_method
    def outlineViewSelectionDidChange_(self, notification) -> None:
        selection = []
        current_index = self.selectedRowIndexes.firstIndex
        for i in range(self.selectedRowIndexes.count):
            selection.append(self.itemAtRow(current_index).attrs['node'])
            current_index = self.selectedRowIndexes.indexGreaterThanIndex(current_index)

        if not self.interface.multiple_select:
            try:
                self.interface._selection = selection[0]
            except IndexError:
                self.interface._selection = None
        else:
            self.interface._selection = selection

        if notification.object.selectedRow == -1:
            selected = None
        else:
            selected = self.itemAtRow(notification.object.selectedRow).attrs['node']

        if self.interface.on_select:
            self.interface.on_select(self.interface, node=selected)


class Tree(Widget):
    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Create the Tree widget
        self.tree = TogaTree.alloc().init()
        self.tree.interface = self.interface
        self.tree._impl = self
        self.tree.columnAutoresizingStyle = NSTableViewColumnAutoresizingStyle.Uniform
        self.tree.usesAlternatingRowBackgroundColors = True

        self.tree.allowsMultipleSelection = self.interface.multiple_select

        # Create columns for the tree
        self.columns = []
        # Cocoa identifies columns by an accessor; to avoid repeated
        # conversion from ObjC string to Python String, create the
        # ObjC string once and cache it.
        self.column_identifiers = {}
        for i, (heading, accessor) in enumerate(zip(self.interface.headings, self.interface._accessors)):

            column_identifier = at(accessor)
            self.column_identifiers[id(column_identifier)] = accessor
            column = NSTableColumn.alloc().initWithIdentifier(column_identifier)
            # column.editable = False
            column.midWidth = 100
            # if self.interface.sorting:
            #     sort_descriptor = NSSortDescriptor.sortDescriptorWithKey(column_identifier, ascending=True)
            #     column.sortDescriptorPrototype = sort_descriptor
            self.tree.addTableColumn(column)
            self.columns.append(column)

            column.headerCell.stringValue = heading

        # Put the tree arrows in the first column.
        self.tree.outlineTableColumn = self.columns[0]

        self.tree.delegate = self.tree
        self.tree.dataSource = self.tree

        # Embed the tree view in the scroll view
        self.native.documentView = self.tree

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.tree.reloadData()

    def insert(self, parent, index, item):

        # set parent = None if inserting to the root item
        index_set = NSIndexSet.indexSetWithIndex(index)
        if parent is self.interface.data:
            parent = None
        else:
            parent = getattr(parent, '_impl', None)

        self.tree.insertItemsAtIndexes(
            index_set,
            inParent=parent,
            withAnimation=NSTableViewAnimation.SlideDown.value
        )

    def change(self, item):
        try:
            self.tree.reloadItem(item._impl)
        except AttributeError:
            pass

    def remove(self, item):
        try:
            index = self.tree.childIndexForItem(item._impl)
        except AttributeError:
            pass
        else:
            index_set = NSIndexSet.indexSetWithIndex(index)
            parent = self.tree.parentForItem(item._impl)
            self.tree.removeItemsAtIndexes(
                index_set,
                inParent=parent,
                withAnimation=NSTableViewAnimation.SlideUp.value
            )

    def clear(self):
        self.tree.reloadData()

    def set_on_select(self, handler):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
