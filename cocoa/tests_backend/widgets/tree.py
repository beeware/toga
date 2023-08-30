import asyncio

from pytest import skip
from rubicon.objc import NSPoint

from toga_cocoa.libs import NSEventType, NSOutlineView, NSScrollView

from .base import SimpleProbe
from .properties import toga_color

NSEventModifierFlagCommand = 1 << 20


class TreeProbe(SimpleProbe):
    native_class = NSScrollView
    supports_keyboard_shortcuts = True
    supports_widgets = True

    def __init__(self, widget):
        super().__init__(widget)
        self.native_tree = widget._impl.native_tree
        assert isinstance(self.native_tree, NSOutlineView)

    @property
    def font(self):
        skip("Font changes not implemented for Tree on macOS")

    @property
    def background_color(self):
        if self.native.drawsBackground:
            return toga_color(self.native.backgroundColor)
        else:
            return None

    async def expand_tree(self):
        self.native_tree.expandItem(None, expandChildren=True)
        await asyncio.sleep(0.1)

    def is_expanded(self, node):
        try:
            return self.native_tree.isItemExpanded(node._impl)
        except AttributeError:
            # If there's no _impl, the node hasn't been visualized yet,
            # so it must be collapsed.
            return False

    def item_for_row_path(self, row_path):
        item = self.native_tree.outlineView(
            self.native_tree,
            child=row_path[0],
            ofItem=None,
        )
        for index in row_path[1:]:
            item = self.native_tree.outlineView(
                self.native_tree,
                child=index,
                ofItem=item,
            )
        return item

    def child_count(self, row_path=None):
        if row_path:
            item = self.item_for_row_path(row_path)
        else:
            item = None

        return int(self.native_tree.numberOfChildrenOfItem(item))

    @property
    def column_count(self):
        return len(self.native_tree.tableColumns)

    def assert_cell_content(self, row_path, col, value=None, icon=None, widget=None):
        view = self.native_tree.outlineView(
            self.native_tree,
            viewForTableColumn=self.native_tree.tableColumns[col],
            item=self.item_for_row_path(row_path),
        )
        if widget:
            assert view == widget._impl.native
        else:
            assert str(view.textField.stringValue) == value

            if icon:
                assert view.imageView.image == icon._impl.native
            else:
                assert view.imageView.image is None

    @property
    def max_scroll_position(self):
        return int(self.native.documentView.bounds.size.height) - int(
            self.native.contentView.bounds.size.height
        )

    @property
    def scroll_position(self):
        return int(self.native.contentView.bounds.origin.y)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    @property
    def header_visible(self):
        return self.native_tree.headerView is not None

    @property
    def header_titles(self):
        return [
            str(col.headerCell.stringValue) for col in self.native_tree.tableColumns
        ]

    def column_width(self, col):
        return self.native_tree.tableColumns[col].width

    def row_position(self, row_path):
        # Convert the row path in to an absolute row index
        item = self.native_tree.child(row_path[0], ofItem=None)
        for index in row_path[1:]:
            item = self.native_tree.child(index, ofItem=item)
        row = self.native_tree.rowForItem(item)

        # Pick a point half way across horizontally, and half way down the row,
        # taking into account the size of the rows and the header
        row_height = self.native_tree.rowHeight
        return self.native_tree.convertPoint(
            NSPoint(
                self.width / 2,
                (row * row_height) + (row_height / 2),
            ),
            toView=None,
        )

    async def select_all(self):
        await self.type_character("A", modifierFlags=NSEventModifierFlagCommand),

    async def select_row(self, row_path, add=False):
        point = self.row_position(row_path)
        # Table maintains an inner mouse event loop, so we can't
        # use the "wait for another event" approach for the mouse events.
        # Use a short delay instead.
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            point,
            delay=0.1,
            modifierFlags=NSEventModifierFlagCommand if add else 0,
        )
        await self.mouse_event(
            NSEventType.LeftMouseUp,
            point,
            delay=0.1,
            modifierFlags=NSEventModifierFlagCommand if add else 0,
        )

    async def activate_row(self, row_path):
        point = self.row_position(row_path)
        # Table maintains an inner mouse event loop, so we can't
        # use the "wait for another event" approach for the mouse events.
        # Use a short delay instead.
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            point,
            delay=0.1,
        )
        await self.mouse_event(
            NSEventType.LeftMouseUp,
            point,
            delay=0.1,
        )

        # Second click, with a click count.
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            point,
            delay=0.1,
            clickCount=2,
        )
        await self.mouse_event(
            NSEventType.LeftMouseUp,
            point,
            delay=0.1,
            clickCount=2,
        )
