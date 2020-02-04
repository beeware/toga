from pathlib import Path

import toga
from toga.style import Pack
from toga.constants import COLUMN
from toga.sources import Source
from datetime import datetime

# This is a slightly less toy example of a tree view to display
# items in your home directory. To avoid loading everything
# in advance, the content of a folder is loaded dynamically,
# on access. This typically happens when the tree view asks for
# the number of children to decide if it should display an
# expandable row.
#
# In practice, one can use a similar concept of on-access
# loading to fetch data from an API or online resource but
# perform the loading asynchronously.


class LoadingFailedNode:
    """A node to represent failed loading of children"""

    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.name = 'loading failed'
        self.date_modified = ''

    # Methods required for the data source interface
    def __len__(self):
        return 0

    def __getitem__(self, index):
        raise StopIteration

    @staticmethod
    def can_have_children():
        return False


class Node:
    """A node which loads its children on-demand."""

    def __init__(self, path, parent):
        super().__init__()

        self.parent = parent
        self._children = []

        self.path = path
        self._mtime = self.path.stat().st_mtime
        if self.path.is_file():
            self._icon = toga.Icon('resources/file')
        else:
            self._icon = toga.Icon('resources/folder')
        self._did_start_loading = False

    # Methods required for the data source interface
    def __len__(self):
        return len(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def can_have_children(self):
        # this will trigger loading of children, if not yet done
        return len(self.children) > 0

    # Property that returns the first column value as (icon, label)
    @property
    def name(self):
        return self._icon, self.path.name

    # Property that returns modified date as str
    @property
    def date_modified(self):
        return datetime.fromtimestamp(self._mtime).strftime('%d %b %Y at %H:%M')

    # on-demand loading of children
    @property
    def children(self):
        if not self._did_start_loading:
            self._did_start_loading = True
            self.load_children()
        return self._children

    def load_children(self):
        try:
            sub_paths = [p for p in self.path.iterdir()]
            self._children = [Node(p, self) for p in sub_paths]
        except NotADirectoryError:
            self._children = []
        except OSError:
            self._children = [LoadingFailedNode(self)]

    def sort(self, accessor, key=None, reverse=False):

        if accessor == 'date_modified':  # use our own sort function
            def sort_func(child):
                return child._mtime
        elif accessor == 'name':
            def sort_func(child):
                return child.name[1].lower()
        else:  # use the function provided by the user / default
            def sort_func(child):
                # sort according to value of accessor, using the provided sort key
                try:
                    attr = getattr(child, accessor)
                    if isinstance(attr, tuple):
                        icon, value = attr
                    else:
                        value = attr
                    return key(value) if key else value
                except AttributeError:
                    return ''

        # sort all children in hierarchy
        self._children.sort(key=sort_func, reverse=reverse)

        for c in self._children:
            try:
                c.sort(accessor, key, reverse)
            except AttributeError:
                pass


class FileSystemSource(Node, Source):

    def __init__(self, path):
        super().__init__(path, parent=self)
        self.path = path
        self._parent = None
        self._children = []


class ExampleTreeSourceApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        root = Path.home()
        self.fs_source = FileSystemSource(root)

        self.tree = toga.Tree(
            headings=['Name', 'Date Modified'],
            data=self.fs_source,
            style=Pack(flex=1),
            multiple_select=True,
        )

        # Outermost box
        outer_box = toga.Box(
            children=[
                toga.Label('A view of your home directory!', style=Pack(padding=10)),
                self.tree,
            ],
            style=Pack(flex=1, direction=COLUMN)
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleTreeSourceApp('Tree Source', 'org.beeware.widgets.tree_source')


if __name__ == '__main__':
    app = main()
    app.main_loop()
