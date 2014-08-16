from __future__ import print_function, absolute_import, division

from gi.repository import Gtk, cairo

from toga_cassowary.widget import Container as CassowaryContainer


class GtkContainer(Gtk.Fixed):
    def __init__(self, layout_manager):
        super(GtkContainer, self).__init__()
        self.layout_manager = layout_manager

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        width = self.layout_manager.bounding_box.width.value
        # print "PREFERRED WIDTH", width
        return width, width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        height = self.layout_manager.bounding_box.height.value
        # print "PREFERRED HEIGHT", height
        return height, height

    def do_size_allocate(self, allocation):
        # print "Size allocate", allocation.width, 'x', allocation.height, ' @ ', allocation.x, 'x', allocation.y

        self.set_allocation(allocation)

        # Temporarily enforce a size requirement based on the allocation
        with self.layout_manager.layout(allocation.width, allocation.height):

            for widget in self.layout_manager.children:
                # print(widget, widget._bounding_box)
                if not widget._impl.get_visible():
                    print("CHILD NOT VISIBLE")
                else:
                    min_width, preferred_width = widget._width_hint
                    min_height, preferred_height = widget._height_hint

                    x_pos = widget._bounding_box.x.value
                    if widget._expand_horizontal:
                        width = widget._bounding_box.width.value
                    else:
                        x_pos = x_pos + ((widget._bounding_box.width.value - preferred_width) / 2.0)
                        width = preferred_width

                    y_pos = widget._bounding_box.y.value
                    if widget._expand_vertical:
                        height = widget._bounding_box.height.value
                    else:
                        y_pos = y_pos + ((widget._bounding_box.height.value - preferred_height) / 2.0)
                        height = preferred_height

                    child_allocation = cairo.RectangleInt()
                    child_allocation.x = x_pos
                    child_allocation.y = y_pos
                    child_allocation.width = width
                    child_allocation.height = height

                    widget._impl.size_allocate(child_allocation)


class Container(CassowaryContainer):
    def __init__(self):
        super(Container, self).__init__()

    def _create_container(self):
        return GtkContainer(self._layout_manager)

    @property
    def _width_hint(self):
        return self._impl.get_preferred_width()

    @property
    def _height_hint(self):
        return self._impl.get_preferred_height()
