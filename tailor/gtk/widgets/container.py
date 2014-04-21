from gi.repository import Gtk, cairo

from tailor.constraint import LayoutManager
from tailor.gtk.widgets.base import Widget


class TContainer(Gtk.Fixed):
    def __init__(self, layout_manager):
        super(TContainer, self).__init__()
        self.children = []
        self.layout_manager = layout_manager

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        print "PREFERRED WIDTH"
        return 290, 370
        # hint = self.layout_manager.layout(None, None)[self.container]
        # return hint.right.vmin - hint.left.vmin, hint.right.vpref - hint.left.vpref,

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        print "PREFERRED HEIGHT"
        return 100, 150
        # hint = self.layout_manager.layout(None, None)[self.container]
        # return hint.bottom.vmin - hint.top.vmin, hint.bottom.vpref - hint.top.vpref,

    def do_size_allocate(self, allocation):
        print "Size allocate", allocation.width, 'x', allocation.height, ' @ ', allocation.x, 'x', allocation.y
        hints = self.layout_manager.layout(allocation.width, allocation.height)

        for widget, hint in hints.items():
            if widget == self.layout_manager.container:
                print 'LAYOUT CONTAINER'
                self.set_allocation(allocation)
            elif not widget._impl.get_visible():
                print "CHILD NOT VISIBLE"
            else:
                print "CHILD", widget

                child_allocation = cairo.RectangleInt()
                child_allocation.x = hint.left.vpref
                child_allocation.y = hint.top.vpref
                child_allocation.width = hint.right.vpref - hint.left.vpref
                child_allocation.height = hint.bottom.vpref - hint.top.vpref

                widget._impl.size_allocate(child_allocation)


class Container(Widget):
    def __init__(self):
        super(Container, self).__init__()
        self._layout_manager = LayoutManager(self)
        self._impl = TContainer(self._layout_manager)
        self._children = []
        self._constraints = []

    def add(self, widget):
        self._layout_manager.reset()
        self._children.append(widget)
        self._impl.add(widget._impl)

    def constrain(self, constraint):
        "Add the given constraint to the widget."
        self._layout_manager.reset()
        self._constraints.append(constraint)
