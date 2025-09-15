from toga_web.libs import create_proxy

from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, interface):
        super().__init__(interface)
        self.native.addEventListener("scroll", create_proxy(self.dom_onscroll))

    def create(self):
        self._horizontal_enabled = True
        self._vertical_enabled = True

        self.native = self._create_native_widget(
            "div",
            classes=["container"],
        )
        self._content_div = self._create_native_widget(
            "div",
            classes=["toga-scroll-content"],
        )
        self.native.appendChild(self._content_div)
        self._update_overflow()

    def set_content(self, content_impl):
        while self._content_div.firstChild:
            self._content_div.removeChild(self._content_div.firstChild)

        if content_impl is not None:
            self._content_div.appendChild(content_impl.native)

    def _update_overflow(self):
        self.native.style.overflowX = "auto" if self._horizontal_enabled else "hidden"
        self.native.style.overflowY = "auto" if self._vertical_enabled else "hidden"

    def get_horizontal(self):
        return self._horizontal_enabled

    def set_horizontal(self, value):
        self._horizontal_enabled = bool(value)
        self._update_overflow()

    def get_vertical(self):
        return self._vertical_enabled

    def set_vertical(self, value):
        self._vertical_enabled = bool(value)
        self._update_overflow()

    def get_max_horizontal_position(self):
        return max(0, self.native.scrollWidth - self.native.clientWidth)

    def get_max_vertical_position(self):
        return max(0, self.native.scrollHeight - self.native.clientHeight)

    def get_horizontal_position(self):
        return self.native.scrollLeft

    def get_vertical_position(self):
        return self.native.scrollTop

    def set_position(self, horizontal, vertical):
        if self._horizontal_enabled:
            horizontal = max(
                0, min(int(horizontal), self.get_max_horizontal_position())
            )
        else:
            horizontal = self.native.scrollLeft

        if self._vertical_enabled:
            vertical = max(0, min(int(vertical), self.get_max_vertical_position()))
        else:
            vertical = self.native.scrollTop

        self.native.scrollTo(horizontal, vertical)

    def dom_onscroll(self, _evt):
        self.interface.on_scroll()
