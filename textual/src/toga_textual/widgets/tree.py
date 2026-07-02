import warnings

from textual._context import active_app
from textual.widgets import Tree as TextualTree
from travertino.size import at_least

from .base import Widget


class TogaTree(TextualTree):
    def __init__(self, impl):
        super().__init__("", data=None)
        self.interface = impl.interface
        self.impl = impl
        self.show_root = False
        self.auto_expand = False

    def on_mount(self):
        self.impl.on_mount()

    def on_tree_node_selected(self, event: TextualTree.NodeSelected):
        if event.node._tree is self and not self.impl._suppress_select_events:
            self.impl.select_node(event.node.data)


class Tree(Widget):
    def create(self):
        self.native = TogaTree(self)
        self._selection = [] if self.interface.multiple_select else None
        self._tree_width = self.interface._MIN_WIDTH
        self._column_widths = []
        self._suppress_select_events = 0

    def _native_is_ready(self):
        return self.native.is_attached and self.interface.app is not None

    def _ensure_active_app(self):
        if self.interface.app is not None:
            active_app.set(self.interface.app._impl.native)

    def _default_column_widths(self):
        count = len(self.interface._columns)
        if count == 0:
            return []

        width = max(self._tree_width, count)
        base_width, remainder = divmod(round(width), count)
        return [
            base_width + (1 if index < remainder else 0)
            for index in range(count)
        ]

    def _ensure_column_widths(self):
        count = len(self.interface._columns)
        if count == 0:
            self._column_widths = []
        elif len(self._column_widths) != count:
            self._column_widths = self._default_column_widths()

    def cell_text(self, node, column, warn=True):
        if column.widget(node) is not None:
            if warn:
                warnings.warn(
                    "Textual does not support the use of widgets in cells",
                    stacklevel=2,
                )
            return self.interface.missing_value

        return column.text(node, self.interface.missing_value)

    def cell_icon(self, node, column):
        return column.icon(node)

    def node_label(self, node):
        return "  ".join(
            self.cell_text(node, column)
            for column in self.interface._columns
        )

    def _add_native_node(self, parent_impl, node, index=None):
        if node.can_have_children():
            node_impl = parent_impl.add(
                self.node_label(node),
                data=node,
                before=index,
                expand=False,
                allow_expand=True,
            )
        else:
            node_impl = parent_impl.add_leaf(
                self.node_label(node),
                data=node,
                before=index,
            )

        node._impl = node_impl

        for child in node:
            self._add_native_node(node_impl, child)

        return node_impl

    def _clear_node_impls(self, node):
        node._impl = None
        for child in node:
            self._clear_node_impls(child)

    def _rebuild_native_tree(self):
        if not self._native_is_ready():
            return

        self._ensure_active_app()
        for node in self.interface.data:
            self._clear_node_impls(node)

        self.native.clear()
        self.native.root.expand()

        for index, node in enumerate(self.interface.data):
            self._add_native_node(self.native.root, node, index=index)

        self._sync_native_selection()

    def _sync_native_selection(self):
        if not self._native_is_ready():
            return

        if self.interface.multiple_select:
            node = self._selection[-1] if self._selection else None
        else:
            node = self._selection

        self._suppress_select_events += 1
        try:
            self.native.move_cursor(None if node is None else node._impl)
        finally:
            self._suppress_select_events -= 1

    def _contains_node(self, root, node):
        if root is node:
            return True
        return any(self._contains_node(child, node) for child in root)

    def _clear_removed_selection(self, removed_node):
        if self.interface.multiple_select:
            self._selection = [
                node
                for node in self._selection
                if not self._contains_node(removed_node, node)
            ]
        elif self._selection is not None and self._contains_node(
            removed_node,
            self._selection,
        ):
            self._selection = None

    def on_mount(self):
        self._rebuild_native_tree()

    def focus(self):
        self.native.app.set_focus(self.native)

    def change_source(self, source):
        self._selection = [] if self.interface.multiple_select else None
        self._rebuild_native_tree()

    # Listener Protocol implementation

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item, parent=None):
        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item, parent=parent)

    def source_insert(self, *, index, item, parent=None):
        if self._native_is_ready():
            self._ensure_active_app()
            parent_impl = self.native.root if parent is None else parent._impl
            if parent is not None:
                parent_impl.allow_expand = True
            self._add_native_node(parent_impl, item, index=index)
            self._sync_native_selection()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        if self._native_is_ready():
            self._ensure_active_app()
            item._impl.set_label(self.node_label(item))

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item, parent=None):
        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item, parent=parent)

    def source_remove(self, *, index, item, parent=None):
        self._clear_removed_selection(item)

        if self._native_is_ready():
            self._ensure_active_app()
            item._impl.remove()
            self._clear_node_impls(item)
            self._sync_native_selection()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        self._selection = [] if self.interface.multiple_select else None

        if self._native_is_ready():
            self._ensure_active_app()
            self.native.clear()

    def get_selection(self):
        return self._selection

    def select_node(self, node, add=False):
        if node is None:
            self._selection = [] if self.interface.multiple_select else None
        elif self.interface.multiple_select:
            if add:
                if node in self._selection:
                    self._selection.remove(node)
                else:
                    self._selection.append(node)
            else:
                self._selection = [node]
        else:
            self._selection = node

        self._sync_native_selection()
        self.interface.on_select()

    def activate_node(self, node):
        if node is not None:
            self.select_node(node)
            self.interface.on_activate(node=node)

    def expand_node(self, node):
        if node.can_have_children() and self._native_is_ready():
            self._ensure_active_app()
            node._impl.expand_all()

    def expand_all(self):
        if self._native_is_ready():
            self._ensure_active_app()
            self.native.root.expand_all()

    def collapse_node(self, node):
        if node.can_have_children() and self._native_is_ready():
            self._ensure_active_app()
            node._impl.collapse()

    def collapse_all(self):
        if self._native_is_ready():
            self._ensure_active_app()
            self.native.root.collapse_all()
            self.native.root.expand()

    def insert_column(self, index, column):
        self._column_widths = self._default_column_widths()
        self._rebuild_native_tree()

    def remove_column(self, index):
        self._column_widths = self._default_column_widths()
        self._rebuild_native_tree()

    def column_width(self, index):
        self._ensure_column_widths()
        return self._column_widths[index]

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self._tree_width = width
        self._column_widths = self._default_column_widths()

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            self.scale_in_vertical(self.interface._MIN_HEIGHT)
        )
