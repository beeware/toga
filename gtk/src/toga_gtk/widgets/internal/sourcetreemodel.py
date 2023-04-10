import copy

from toga_gtk.libs import GObject, Gtk


class SourceTreeModel(GObject.Object, Gtk.TreeModel):
    """A full Gtk.TreeModel implementation backed by a toga.source.ListSource
    or toga.source.TreeSource.

    It stores a reference to every node in the source.
    TODO: If the source is a TreeSource, it uses the Node._parent attribute.
    Maybe an method could be added (like index()) to the TreeSource to access it.
    """

    def __init__(self, columns, is_tree):
        """
        Args:
            columns (list(dict(str, any))): the columns excluding first column which is always the row object.
                each ``dict`` must have:
                 - an ``attr`` entry, with a string value naming the attribute to get from the row
                 - a ``type`` entry, with the column type (``str``, ``Gtk.Pixbuf``, ...)
            is_tree (bool): the model must know if it's for a tree or a list to set flags
        """
        super().__init__()
        self.source = None
        self.columns = columns
        self.is_tree = is_tree
        # by storing the row and calling index later, we can opt-in for this performance
        # boost and don't have to track iterators (we would have to if we stored indices).
        self.flags = Gtk.TreeModelFlags.ITERS_PERSIST
        if not is_tree:
            self.flags |= Gtk.TreeModelFlags.LIST_ONLY
        # stamp will be increased each time the data source changes. -1 is always invalid
        self.stamp = 0
        # the pool maps integer (the only thing we can store in Gtk.TreeIter) to row object.
        # It's purged on data source change and on remove
        self.pool = {}
        # roots is an array of root elements in the data source.
        # they are kept here to support the clear() notification without parameters
        self.roots = (
            []
        )  # maybe a deque would be more efficient. This can be changed later
        self.index_in_parent = {}

    def clear(self):
        """Called from toga impl widget."""
        if self.is_tree:
            self._remove_children_rec([], self.roots)
        else:
            for i, node in reversed(list(enumerate(self.roots))):
                self.row_deleted(Gtk.TreePath.new_from_indices([i]))
                self._clear_user_data(node)

    def change_source(self, source):
        """Called from toga impl widget."""
        if self.source:
            self.clear()
        self.source = source
        self.stamp += 1

    def insert(self, row):
        """Called from toga impl widget."""
        it = self._create_iter(user_data=row)
        index = self.source.index(row)
        if not self.is_tree or self.is_root(row):
            self.roots.insert(index, row)
            parent = self.source
        else:
            parent = row._parent
        self._update_index_in_parent(parent, index)
        parent_indices = self._get_indices(parent) if parent is not self.source else []
        if self.is_tree and not self.is_root(row) and (len(row._parent) == 1):
            parent_it = self._create_iter(user_data=row._parent)
            parent_p = Gtk.TreePath.new_from_indices(parent_indices)
            self.row_has_child_toggled(parent_p, parent_it)
        p = Gtk.TreePath.new_from_indices(parent_indices + [index])
        self.row_inserted(p, it)

    def change(self, row):
        """Called from toga impl widget."""
        indices = self._get_indices(row)
        self.row_changed(
            Gtk.TreePath.new_from_indices(indices), self._create_iter(user_data=row)
        )

    def remove(self, row, index, parent=None):
        """Called from toga impl widget."""
        # todo: could get index from index_in_parent
        if parent is None:
            indices = []
            del self.roots[index]
            parent = self.source
        else:
            indices = self._get_indices(parent)
        indices.append(index)
        if self.is_tree and row.can_have_children():
            self._remove_children_rec(indices, row)
        self.row_deleted(Gtk.TreePath.new_from_indices(indices))
        self._clear_user_data(row)
        self._update_index_in_parent(parent, index)
        if self.is_tree and parent is not None and (len(parent) == 0):
            parent_it = self._create_iter(user_data=parent)
            parent_indices = copy.copy(indices[:-1])
            parent_p = Gtk.TreePath.new_from_indices(parent_indices)
            self.row_has_child_toggled(parent_p, parent_it)

    def _remove_children_rec(self, indices, parent):
        for i, node in reversed(list(enumerate(parent))):
            indices.append(i)
            if node.can_have_children():
                self._remove_children_rec(indices, node)
            self.row_deleted(Gtk.TreePath.new_from_indices(indices))
            self._clear_user_data(node)
            del indices[-1]

    def path_to_node(self, row):
        """Called from toga impl widget."""
        indices = self._get_indices(row)
        if indices is not None:
            return Gtk.TreePath.new_from_indices(indices)
        return Gtk.TreePath()

    def do_get_column_type(self, index_):
        """Gtk.TreeModel."""
        if index_ == 0:
            return object
        return self.columns[index_ - 1]["type"]

    def do_get_flags(self):
        """Gtk.TreeModel."""
        return self.flags

    def do_get_iter(self, path):
        """Gtk.TreeModel."""
        indices = path.get_indices()
        r = self._get_row(indices)
        if r is None:
            return False, Gtk.TreeIter(stamp=-1)
        return True, self._create_iter(user_data=r)

    def do_get_n_columns(self):
        """Gtk.TreeModel."""
        return len(self.columns) + 1

    def do_get_path(self, iter_):
        """Gtk.TreeModel."""
        if iter_ is None or iter_.stamp != self.stamp:
            return Gtk.TreePath()
        r = self._get_user_data(iter_)
        indices = self._get_indices(r)
        if indices is None:
            return Gtk.TreePath()
        return Gtk.TreePath.new_from_indices(indices)

    def do_get_value(self, iter_, column):
        """Gtk.TreeModel."""
        if iter_ is None or iter_.stamp != self.stamp:
            return None
        row = self._get_user_data(iter_)
        if column == 0:
            return row
        if row is None:
            return None

        # workaround icon+name tuple breaking gtk tree
        ret = getattr(row, self.columns[column - 1]["attr"])
        if isinstance(ret, tuple):
            ret = ret[1]
        return ret

    def do_iter_children(self, parent):
        """Gtk.TreeModel."""
        if parent is None:
            r = self.source
        else:
            r = self._get_user_data(parent)
        if self._row_has_child(r, 0):
            return True, self._create_iter(user_data=r[0])
        return False, Gtk.TreeIter(stamp=-1)

    def do_iter_has_child(self, iter_):
        """Gtk.TreeModel."""
        if iter_ is None:
            return len(self.source) > 0
        if iter_.stamp == self.stamp:
            r = self._get_user_data(iter_)
            ret = self._row_has_child(r, 0)
            return ret
        return False

    def do_iter_n_children(self, iter_):
        """Gtk.TreeModel."""
        if iter_ is None:
            r = self.source
        elif iter_.stamp == self.stamp:
            r = self._get_user_data(iter_)
        else:
            r = None
        if self._row_has_child(r, 0):
            return len(r)
        return 0

    def do_iter_next(self, iter_):
        """Gtk.TreeModel."""
        if iter_ is not None and iter_.stamp == self.stamp:
            r = self._get_user_data(iter_)
            if r is not None:
                if self.is_tree:
                    parent = r._parent or self.source
                else:
                    parent = self.source
                if len(parent) and r is not parent[-1]:
                    try:
                        index = self.index_in_parent[r]
                        self._set_user_data(iter_, parent[index + 1])
                        return True
                    except ValueError:
                        pass
        if iter_ is not None:
            iter_.stamp = -1  # invalidate
        return False

    def do_iter_previous(self, iter_):
        """Gtk.TreeModel."""
        if iter_ is not None and iter_.stamp == self.stamp:
            r = self._get_user_data(iter_)
            if r is not None:
                if self.is_tree:
                    parent = r._parent or self.source
                else:
                    parent = self.source
                if len(parent) and r is not parent[0]:
                    try:
                        index = self.index_in_parent[r]
                        self._set_user_data(iter_, parent[index - 1])
                        return True
                    except ValueError:
                        pass
        if iter_ is not None:
            iter_.stamp = -1
        return False

    def do_iter_nth_child(self, parent, n):
        """Gtk.TreeModel."""
        if parent is None:
            r = self.source
        elif parent.stamp != self.stamp:
            return False, Gtk.TreeIter(stamp=-1)
        else:
            r = self._get_user_data(parent)
        if self._row_has_child(r, n):
            return True, self._create_iter(user_data=r[n])
        return False, Gtk.TreeIter(stamp=-1)

    def do_iter_parent(self, child):
        """Gtk.TreeModel."""
        if not self.is_tree or child is None or (child.stamp != self.stamp):
            return False, Gtk.TreeIter(stamp=-1)
        r = self._get_user_data(child)
        if r is None or r is self.source:
            return False, Gtk.TreeIter(stamp=-1)
        parent = r._parent or self.source
        if parent is self.source:
            return False, Gtk.TreeIter(stamp=-1)
        return True, self._create_iter(user_data=parent)

    def do_ref_node(self, iter_):
        """Gtk.TreeModel."""
        pass

    def do_unref_node(self, iter_):
        """Gtk.TreeModel."""
        pass

    def _get_row(self, indices):
        if self.source is None:
            return None
        s = self.source
        if self.is_tree:
            for i in indices:
                if s.can_have_children():
                    if i < len(s):
                        s = s[i]
                    else:
                        return None
                else:
                    return None
            return s
        else:
            if len(indices) == 1:
                i = indices[0]
                if i < len(s):
                    return s[i]
            return None

    def _get_indices(self, row):
        if row is None or self.source is None:
            return None
        if self.is_tree:
            indices = []
            while row not in (None, self.source):
                indices.insert(0, self.index_in_parent[row])
                row = row._parent
            return indices
        else:
            return [self.source.index(row)]

    def _row_has_child(self, row, n):
        return (
            row is not None
            and ((self.is_tree and row.can_have_children()) or (row is self.source))
            and len(row) > n
        )

    def _set_user_data(self, it, user_data):
        data_id = id(user_data)
        it.user_data = data_id
        self.pool[data_id] = user_data

    def _get_user_data(self, it):
        return self.pool.get(it.user_data)

    def _clear_user_data(self, user_data):
        data_id = id(user_data)
        if data_id in self.pool:
            del self.pool[data_id]
        if user_data in self.index_in_parent:
            del self.index_in_parent[user_data]

    def _create_iter(self, user_data):
        it = Gtk.TreeIter()
        it.stamp = self.stamp
        self._set_user_data(it, user_data)
        return it

    def _update_index_in_parent(self, parent, index):
        for i in range(index, len(parent)):
            self.index_in_parent[parent[i]] = i

    def is_root(self, node):
        return node._parent in (None, self.source)
