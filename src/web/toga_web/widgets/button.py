from toga_web.dom import register_handler

from .base import Widget

class Button(Widget):
    def __html__(self):
        return """
            <button id="toga_{id}" class="toga button btn-block" style="{style}" pys-onClick="dom_handle">
            {label}
            </button>
        """.format(
            id=self.interface.id,
            label=self.interface.label,
            style=self.interface.style.__css__(),
        )

    def create(self):
        pass

    def set_label(self, label):
        pass

    def set_enabled(self, value):
        pass

    def set_background_color(self, value):
        pass

    def set_on_press(self, handler):
        register_handler('mouse_press', self.interface, handler)

    def rehint(self):
        pass
