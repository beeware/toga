from travertino.size import at_least


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.viewport = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        self._container.native.add(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(self.interface.enabled)

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        # No implementation required here; the new sizing will be picked up
        # by the box's allocation handler.
        pass

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        # Rules: any given widget must be invisible if...
        # 1. it's visibility style property equals "hidden"
        # 2. it has an invisible anscestor
        #
        # set_hidden calls are expected from two sources:
        # 1. the style engine, when self.interface.style.visibility is changed
        # 2. this widget's parent, when it's style.visibility is changed
        # Therefore, if the provided argument of set_hidden does not match this
        # widget's current state, the call is assumed to have originated from
        # the parent
        #
        # Note on iterating childring:
        # Container widgets store children in their `content` property and
        # their `children` property will always return []. Iterating a
        # container's `children` property is a do-nothing, but that is
        # acceptible in this case because hiding a container will in
        # turn hide the native container, which will cause all native children
        # to be hidden.
        #
        # In GTK, all widgets are initially hidden

        my_interface_hidden = (self.interface.style.visibility == "hidden")

        if self.native:
            if my_interface_hidden or hidden:
                # if self.native is a container widget, each native child will
                # be hidden too
                self.native.hide()

                if self.interface.can_have_children:
                    for child in self.interface.children:
                        child._impl.set_hidden(True)

            else:
                # if self.native is a container widget, each native child will
                # be shown (if it is not hidden by its own style property)
                self.native.show()

                if self.interface.can_have_children:
                    for child in self.interface.children:
                        child._impl.set_hidden(False)
        else:
            raise Exception("cannot hide widget: no native widget to hide")

    def set_font(self, font):
        # By default, fon't can't be changed
        pass

    def set_color(self, color):
        # By default, color can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed
        pass

    # INTERFACE

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(),
        #     self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = at_least(height[0])
