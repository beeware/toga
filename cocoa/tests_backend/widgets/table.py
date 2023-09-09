from pytest import skip
from rubicon.objc import NSPoint

from toga_cocoa.libs import NSEventType, NSScrollView, NSTableView

from .base import SimpleProbe
from .properties import toga_color

NSEventModifierFlagCommand = 1 << 20


class TableProbe(SimpleProbe):
    native_class = NSScrollView
    supports_icons = 2  # All columns
    supports_keyboard_shortcuts = True
    supports_widgets = True

    def __init__(self, widget):
        super().__init__(widget)
        self.native_table = widget._impl.native_table
        assert isinstance(self.native_table, NSTableView)

    @property
    def font(self):
        skip("Font changes not implemented for Tree on macOS")

    @property
    def background_color(self):
        if self.native.drawsBackground:
            return toga_color(self.native.backgroundColor)
        else:
            return None

    @property
    def row_count(self):
        return int(self.native_table.numberOfRowsInTableView(self.native_table))

    @property
    def column_count(self):
        return len(self.native_table.tableColumns)

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        view = self.native_table.tableView(
            self.native_table,
            viewForTableColumn=self.native_table.tableColumns[col],
            row=row,
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
        return self.native_table.headerView is not None

    @property
    def header_titles(self):
        return [
            str(col.headerCell.stringValue) for col in self.native_table.tableColumns
        ]

    def column_width(self, col):
        return self.native_table.tableColumns[col].width

    def row_position(self, row):
        # Pick a point half way across horizontally, and half way down the row,
        # taking into account the size of the rows and the header
        row_height = self.native_table.rowHeight
        return self.native_table.convertPoint(
            NSPoint(
                self.width / 2,
                (row * row_height) + (row_height / 2),
            ),
            toView=None,
        )

    async def select_all(self):
        await self.type_character("A", modifierFlags=NSEventModifierFlagCommand),

    async def select_row(self, row, add=False):
        point = self.row_position(row)
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

    async def activate_row(self, row):
        point = self.row_position(row)
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
