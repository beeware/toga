import os
import subprocess
import platform
from datetime import datetime
from pathlib import Path

import toga
from toga.constants import COLUMN
from toga.sources import TreeSource, Node
from toga.style import Pack

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

    def __init__(self):
        super().__init__(name='loading failed', date_modified='')

    # Methods required for the data source interface
    def __len__(self):
        return 0

    def __getitem__(self, index):
        raise StopIteration

    @staticmethod
    def can_have_children():
        return False


class FileSystemNode(Node):
    """A node which loads its children on-demand."""

    def __init__(self, path):

        mtime = path.stat().st_mtime
        date_str = datetime.fromtimestamp(mtime).strftime('%d %b %Y at %H:%M')

        if path.is_file():
            icon = toga.Icon('resources/file')
        else:
            icon = toga.Icon('resources/folder')

        super().__init__(name=path.name, icon=icon, date_modified=date_str, selected=1)

        self._path = path
        self._did_start_loading = False
        self._children = []

    def __repr__(self):
        return "<Node {0}>".format(self._path)

    # Methods required for the data source interface
    def __len__(self):
        return len(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def can_have_children(self):
        # this will trigger loading of children, if not yet done
        return len(self.children) > 0

    # on-demand loading of children
    @property
    def children(self):
        if not self._did_start_loading:
            self._did_start_loading = True
            self.load_children()
        return self._children

    def load_children(self):
        try:
            sub_paths = [p for p in self._path.iterdir()]
            for path in sub_paths:
                node = FileSystemNode(path)
                node._parent = self
                node._source = self._source
                self._children.append(node)
        except NotADirectoryError:
            self._children = []
        except OSError:
            node = LoadingFailedNode()
            node._parent = self
            node._source = self._source
            self._children = [node]


class FileSystemSource(TreeSource):
    def __init__(self, path):
        super().__init__(data=[], accessors=["icon", "name", "date_modified"])
        self._path = path
        self._load_children()

    def _load_children(self):
        try:
            sub_paths = [p for p in self._path.iterdir()]
            for path in sub_paths:
                node = FileSystemNode(path)
                node._source = self
                self._roots.append(node)
        except NotADirectoryError:
            self._roots = []
        except OSError:
            node = LoadingFailedNode()
            node._source = self
            self._roots = [node]


class ExampleTreeSourceApp(toga.App):
    def selection_handler(self, widget, node):
        # A node is a dictionary of the last item that was clicked in the tree.
        # node['node'].path would get you the file path to only that one item.
        # self.label.text = f'Selected {node["node"].path}'

        # If you iterate over widget.selection, you can get the names and the
        # paths of everything selected (if multiple_select is enabled.)
        # filepaths = [node.path for node in widget.selection]
        if isinstance(widget.selection, list):
            files = len(widget.selection)
        else:
            files = 0 if widget.selection is None else 1
        if files == 0:
            self.label.text = 'A view of the current directory!'
        elif files == 1:
            self.label.text = 'You selected {0} item'.format(files)
        else:
            self.label.text = 'You selected {0} items'.format(files)

    def double_click_handler(self, widget, node):
        # open the file or folder in the platform's default app
        self.label.text = 'You started {0}'.format(node.path)
        if platform.system() == 'Darwin':
            subprocess.call(('open', node.path))
        elif platform.system() == 'Windows':
            os.startfile(node.path)
        else:
            subprocess.call(('xdg-open', node.path))

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.fs_source = FileSystemSource(Path.cwd())

        col0 = toga.Tree.Column(title="Name", icon="icon", text="name", editable=False)
        col1 = toga.Tree.Column(title="Date Modified", text="date_modified", editable=False)
        col2 = toga.Tree.Column(title="Selected", checked_state="selected", editable=False)

        self.tree = toga.Tree(
            columns=[col0, col1, col2],
            data=self.fs_source,
            style=Pack(flex=1),
            multiple_select=True,
            on_select=self.selection_handler,
            on_double_click=self.double_click_handler
        )
        self.label = toga.Label('A view of the current directory!', style=Pack(padding=10))

        # Outermost box
        outer_box = toga.Box(
            children=[
                self.label,
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
