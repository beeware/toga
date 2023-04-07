from toga_web.libs import create_element


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None

        self.create()

    def _create_native_widget(
        self, tag, classes=None, content=None, children=None, **properties
    ):
        """Create a DOM element representing a native widget.

        The ID and style of the widget will be automatically set;
        ``toga``, and the name of the widget class (in lower case)
        will be added as a class name on the widget.

        :param widget: The web implementation being created.
        :param tag: The HTML tag for t
        :param classes: (Optional) A list of classes to attach to the
            new element. Two widgets
        :param content: (Optional) The innerHTML content of the element.
        :param children: (Optional) A list of direct descendents to add to
            the element.
        :param properties: Any additional properties that should be set.
            These *must* be HTML DOM properties (e.g., ``readOnly``);
            they cannot be events or methods.
        :returns: A newly created DOM element.
        """
        if classes is None:
            classes = []

        classes = ["toga", self.interface.__class__.__name__.lower()] + classes

        native = create_element(
            tag,
            id=f"toga_{self.interface.id}",
            classes=classes,
            style=self.interface.style.__css__(),
            content=content,
            children=children,
            **properties,
        )

        return native

    def create(self):
        raise NotImplementedError()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def viewport(self):
        return self._container

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container

        for child in self.interface.children:
            child._impl.container = container

    def get_enabled(self):
        return not self.native.disabled

    def set_enabled(self, value):
        self.native.disabled = not value

    def focus(self):
        self.interface.factory.not_implemented("Widget.focus()")

    def get_tab_index(self):
        self.interface.factory.not_implementated("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implementated("Widget.set_tab_index()")

    ######################################################################
    # APPLICATOR
    #
    # Web style is a little different to other platforms; we if there's
    # any change, we can just re-set the CSS styles and the browser
    # will reflect those changes as needed.
    ######################################################################

    def _reapply_style(self):
        self.native.style = self.interface.style.__css__()

    def set_bounds(self, x, y, width, height):
        self._reapply_style()

    def set_alignment(self, alignment):
        self._reapply_style()

    def set_hidden(self, hidden):
        self._reapply_style()

    def set_font(self, font):
        self._reapply_style()

    def set_color(self, color):
        self._reapply_style()

    def set_background_color(self, color):
        self._reapply_style()

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        pass

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        self._reapply_style()

    def rehint(self):
        pass
