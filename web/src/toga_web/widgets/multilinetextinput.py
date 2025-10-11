from travertino.colors import TRANSPARENT
from travertino.size import at_least

from toga_web.libs import create_proxy

from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-textarea")
        self.native.addEventListener("sl-input", create_proxy(self._on_input))

        def _after_render(_):
            self.native.shadowRoot.querySelector("textarea").style.resize = "none"

        self.native.updateComplete.then(create_proxy(_after_render))

    def _on_input(self, event):
        self.interface.on_change()

    def get_value(self):
        return self.native.value or ""

    def set_value(self, value):
        self.native.value = "" if value is None else str(value)
        self.interface.on_change()

    def get_placeholder(self):
        return self.native.placeholder or ""

    def set_placeholder(self, value):
        self.native.placeholder = value or ""

    def get_readonly(self):
        return bool(self.native.readonly)

    def set_readonly(self, value):
        self.native.readonly = bool(value)

    def get_enabled(self):
        return not bool(self.native.disabled)

    def set_enabled(self, value):
        self.native.disabled = not bool(value)

    def _to_css_color(self, value: object) -> str:
        if value is None or value is TRANSPARENT:
            return ""
        try:
            return str(value)
        except Exception:
            return ""

    def set_background_color(self, color):
        css = self._to_css_color(color)

        def _apply(_):
            inner = self.native.shadowRoot.querySelector("textarea")
            if inner:
                if css:
                    inner.style.setProperty("background", css)
                else:
                    inner.style.removeProperty("background")

        self.native.updateComplete.then(create_proxy(_apply))

    def set_color(self, color):
        css = self._to_css_color(color)

        def _apply(_):
            inner = self.native.shadowRoot.querySelector("textarea")
            if inner:
                if css:
                    inner.style.setProperty("color", css)
                else:
                    inner.style.removeProperty("color")

        self.native.updateComplete.then(create_proxy(_apply))

    def set_text_align(self, value):
        mapping = {0: "left", 1: "right", 2: "center", 3: "justify"}
        css_align = mapping.get(value, value if isinstance(value, str) else "left")

        def _apply(_):
            inner = self.native.shadowRoot.querySelector("textarea")
            if inner:
                inner.style.textAlign = css_align

        self.native.updateComplete.then(create_proxy(_apply))

    def set_font(self, font):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_top(self):
        def _go(_):
            inner = self.native.shadowRoot.querySelector("textarea")
            if inner:
                inner.scrollTop = 0

        self.native.updateComplete.then(create_proxy(_go))

    def scroll_to_bottom(self):
        def _go(_):
            inner = self.native.shadowRoot.querySelector("textarea")
            if inner:
                inner.scrollTop = max(0, inner.scrollHeight - inner.clientHeight)

        self.native.updateComplete.then(create_proxy(_go))
