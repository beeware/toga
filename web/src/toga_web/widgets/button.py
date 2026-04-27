from toga_web.libs import create_proxy

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = self._create_native_widget("wa-button")
        self.native.setAttribute("appearance", "outlined")
        self.native.addEventListener("click", create_proxy(self.dom_click))

    def dom_click(self, event):
        self.interface.on_press()

    def get_text(self):
        return self.native.innerHTML

    def set_text(self, text):
        self.native.innerHTML = text

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            self.interface.factory.not_implemented("Button.icon")

    def set_enabled(self, value):
        self.native.disabled = not value

    def set_background_color(self, value):
        pass

    def _reapply_style(self):
        # wa-button (appearance="outlined") sets text color via --wa-color-on-quiet
        # inside its shadow DOM, so the host's inherited `color` doesn't reach the
        # button label. Forward it as a CSS variable so the shadow DOM picks it up.
        css = self.interface.style.__css__()
        if color := self.interface.style.color:
            css += f" --wa-color-on-quiet: {color};"
        self.native.style = css

    def rehint(self):
        pass
