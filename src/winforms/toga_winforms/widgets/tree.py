from toga_winforms.libs import WinForms
from travertino.size import at_least

from .base import Widget


class Tree(Widget):
    def create(self):
        self.native = WinForms.TreeView()
        self.headings = self.interface.headings

    def change_source(self, source):

        self.native.BeginUpdate()

        def create_children(node):
            if node._children is None or len(node._children) == 0:
                # FIXME Works if there is only one accessor. Not sure what the behaviour
                # should be with many accessors
                return WinForms.TreeNode(getattr(node, self.interface._accessors[0]))
            else:
                new_node = WinForms.TreeNode(getattr(node, self.interface._accessors[0]))
                for i, child in enumerate(node._children):
                    new_child_node = create_children(child)
                    new_node.Nodes.Add(new_child_node)
                return new_node

        for node in self.interface.data:
            children = create_children(node)
            self.native.Nodes.Add(children)

        self.native.EndUpdate()
        self.native.ExpandAll()

    def insert(self, parent, index, item):
        print('insert')
        pass

    def change(self, item):
        print('change')
        pass

    def remove(self, item):
        print('remove')
        pass

    def clear(self):
        print('clear')
        pass

    def set_on_select(self, handler):
        print('set on select')
        self.interface.factory.not_implemented('Table.set_on_select()')

    def rehint(self):
        print('rehint')
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
