from gi.repository import Gtk, Gdk


class CSSLayout(Gtk.Fixed):
    def __init__(self, container):
        super().__init__()
        self._interface = container

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        # print("GET PREFERRED WIDTH")
        width = self._interface.content.style.layout.width
        min_width = self._interface.min_width
        if min_width > width:
            width = min_width

        # print(min_width, width)
        return min_width, width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        # height = self.interface.layout.height
        # print("GET PREFERRED HEIGHT")
        height = self._interface.content.style.layout.height
        min_height = self._interface.min_height
        if min_height > height:
            height = min_height

        # print(min_height, height)
        return min_height, height

    def do_size_allocate(self, allocation):
        # print(self._interface, "Container layout", allocation.width, 'x', allocation.height, ' @ ', allocation.x, 'x', allocation.y)
        self.set_allocation(allocation)

        # Force a re-layout of widgets
        self._interface.content._update_layout(
            width=allocation.width,
            height=allocation.height
        )

        # for widget in self.children:
        for widget in self.get_children():
            if not widget.get_visible():
                # print("CHILD NOT VISIBLE", widget._interface)
                pass
            else:
                # print("update ", widget._interface, widget._interface.style.layout)
                child_allocation = Gdk.Rectangle()
                child_allocation.x = widget._interface.style.layout.absolute.left
                child_allocation.y = widget._interface.style.layout.absolute.top
                child_allocation.width = widget._interface.style.layout.width
                child_allocation.height = widget._interface.style.layout.height

                widget.size_allocate(child_allocation)


class Container:
    def __init__(self):
        self._impl = CSSLayout(self)
        self._content = None
        self._min_width = None
        self._min_height = None

    @property
    def min_width(self):
        if self._min_width:
            return self._min_width

        # No cached minimum size; compute it by computing an
        # unhinted layout.
        self._update_layout()
        self._min_width = self._content.style.layout.width
        self._min_height = self._content.style.layout.height
        return self._min_width

    @property
    def min_height(self):
        if self._min_height:
            return self._min_height

        # No cached minimum size; compute it by computing an
        # unhinted layout.
        self._update_layout()
        self._min_width = self._content.style.layout.width
        self._min_height = self._content.style.layout.height
        return self._min_height

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content._container = self

    @property
    def root_content(self):
        return self._content

    @root_content.setter
    def root_content(self, widget):
        self._content = widget
        self._content._container = self

    def _update_layout(self, **style):
        if self._content:
            self._content._update_layout(**style)
