from .base import Widget


class Button(Widget):
    def __html__(self):
        return """
            <button id="toga_{id}" class="toga button btn-block" style="{style}">
            {label}
            </button>
        """.format(
            id=self.interface.id,
            label=self.interface.label,
            style='',
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
        pass

    def rehint(self):
        pass
