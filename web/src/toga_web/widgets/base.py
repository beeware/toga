from abc import ABC, abstractmethod

import js
from pyodide.ffi import JsProxy

from toga_web.libs import create_element, create_proxy


class NativeProxy:
    """Wraps a WebAwesome custom element, buffering attribute sets that happen
    before the element's tag has been defined and the instance upgraded.

    Toga's widget lifecycle creates elements detached from the DOM and
    immediately sets class-defined properties on them (e.g. `wa-switch.checked`).
    Those properties only exist after the browser has (a) loaded the component
    module and called `customElements.define` and (b) upgraded the specific
    element instance. Until then, attribute sets would fail.

    The proxy:
      * buffers pre-upgrade sets in an insertion-ordered dict
      * returns the buffered value (or passes through) on reads
      * once `whenDefined` resolves for the element's tag, force-upgrades the
        (possibly still-disconnected) element with `customElements.upgrade`
        and replays the buffer onto the now-upgraded element
    """

    def __init__(self, element):
        # when mutating these bookkeeping members,
        # call object.__setattr__ to avoid calling our own __setattr__ override
        object.__setattr__(self, "_element", element)
        object.__setattr__(self, "_pending", {})
        object.__setattr__(self, "_upgraded", False)

        tag = element.tagName.lower()
        if tag.startswith("wa-"):

            def on_defined(promise):
                js.customElements.upgrade(element)
                object.__setattr__(self, "_upgraded", True)
                for attr, value in self._pending.items():
                    setattr(element, attr, value)
                self._pending.clear()

            js.customElements.whenDefined(tag).then(create_proxy(on_defined))
        else:
            object.__setattr__(self, "_upgraded", True)

    def unwrap(self):
        """Return the underlying JsProxy element.

        Pyodide unwraps JsProxy arguments automatically when marshaling into
        JS, but it does not unwrap arbitrary Python objects — so callers
        that pass a NativeProxy as an *argument* to a JS method (e.g.
        appendChild, insertBefore) must call unwrap() to hand JS the real Node.
        """
        return self._element

    def __getattr__(self, name):
        # If we're still waiting to be upgraded and we've seen a set, return that value
        if not self._upgraded and name in self._pending:
            return self._pending[name]

        attr = getattr(self._element, name)
        # if we're asking for a JsProxy callable, assume we're going to call it;
        # return wrapper that checks all args and unwraps any NativeProxys
        # to their underlying JsProxy elements
        if isinstance(attr, JsProxy) and callable(attr):

            def _auto_unwrap(*args):
                unwrapped_args = [
                    a.unwrap() if isinstance(a, NativeProxy) else a for a in args
                ]
                return attr(*unwrapped_args)

            return _auto_unwrap

        # otherwise just return what was asked for
        return attr

    def __setattr__(self, name, value):
        if self._upgraded:
            setattr(self._element, name, value)
        else:
            # Pop-then-reinsert so replay order mirrors write order even
            # when the same key is set more than once pre-upgrade.
            self._pending.pop(name, None)
            self._pending[name] = value


class Widget(ABC):
    def __init__(self, interface):
        self.interface = interface
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

        return NativeProxy(native)

    @abstractmethod
    def create(self): ...

    def set_app(self, app):  # noqa B027
        pass

    def set_window(self, window):  # noqa B027
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

    def set_text_align(self, alignment):
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

    def add_child(self, child):  # noqa B027
        pass

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        self._reapply_style()

    def rehint(self):  # noqa B027
        pass
