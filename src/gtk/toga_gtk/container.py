from gi.repository import Gtk, Gdk


class TravertinoLayout(Gtk.Fixed):
    def __init__(self, container):
        super().__init__()
        self._container = container

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        # print("GET PREFERRED WIDTH")
        width = self._container.content.interface.layout.width
        min_width = self._container.min_width
        if min_width > width:
            width = min_width

        # print(min_width, width)
        return min_width, width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        # height = self._container.layout.height
        # print("GET PREFERRED HEIGHT")
        height = self._container.content.interface.layout.height
        min_height = self._container.min_height
        if min_height > height:
            height = min_height

        # print(min_height, height)
        return min_height, height

    def do_size_allocate(self, allocation):
        # print(self._container, "Container layout", allocation.width, 'x', allocation.height, ' @ ', allocation.x, 'x', allocation.y)
        self.set_allocation(allocation)

        # for widget in self.children:
        for widget in self.get_children():
            if not widget.get_visible():
                # print("CHILD NOT VISIBLE", widget.interface)
                pass
            else:
                # print("update ", widget.interface, widget.interface.layout)
                child_allocation = Gdk.Rectangle()
                child_allocation.x = widget.interface.layout.absolute_content_left
                child_allocation.y = widget.interface.layout.absolute_content_top
                child_allocation.width = widget.interface.layout.content_width
                child_allocation.height = widget.interface.layout.content_height

                widget.size_allocate(child_allocation)


class Container:
    def __init__(self):
        self.native = TravertinoLayout(self)
        self._content = None
        self.min_width = 0
        self.min_height = 0

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.container = self
