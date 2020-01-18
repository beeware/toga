import os

import toga
from toga.style import Pack
from toga.constants import COLUMN
from toga.sources import Source
from datetime import datetime


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
        pass

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
        self._mtime = os.stat(self.path).st_mtime
        self._icon = toga.Icon('resources/folder.icns')

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
        return self._icon, os.path.basename(self.path)

    # Property that returns modified date as str
    @property
    def date_modified(self):
        return datetime.fromtimestamp(self._mtime).strftime("%d %b %Y at %H:%M")

    # on-demand loading of children
    @property
    def children(self):
        if not self._did_start_loading:
            self._did_start_loading = True
            self.load_children()
        return self._children

    def load_children(self):
        try:
            names = os.scandir(self.path)
            sub_paths = [os.path.join(self.path, p) for p in names if os.path.isdir(os.path.join(self.path, p))]
            self._children = [Node(p, self) for p in sub_paths]
        except OSError:
            self._children = [LoadingFailedNode(self)]

        for i, child in enumerate(self._children):
            self.notify('insert', parent=self, index=i, item=child)

    def notify(self, notification, **kwargs):
        # pass notifications to parent (which is the actual 'data source')
        self.parent.notify(notification, **kwargs)

    def sort(self, accessor, key=None, reverse=False):

        if accessor == "date_modified":  # use our own sort function
            def sort_func(child):
                return child._mtime
        elif accessor == "name":
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

        # sort all children in hirarchy
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

    def notify(self, notification, **kwargs):
        # send actual notification
        self._notify(notification, **kwargs)


class ExampleTreeSourceApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        root = os.path.abspath(os.sep)
        self.fs_source = FileSystemSource(root)

        self.tree = toga.Tree(
            headings=['Name', 'Date Modified'],
            data=self.fs_source,
            style=Pack(flex=1),
            multiple_select=True,
            sorting=True,
            sort_keys=None,
        )

        # Outermost box
        outer_box = toga.Box(
            children=[
                toga.Label('A list of all your folders!', style=Pack(padding=10)),
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
