from .base import Widget


class Button(Widget):
    def __html__(self):
        return """
            <button id="toga_{id}" class="toga button btn-block" style="{style}">
            {text}
            </button>
        """.format(
            id=self.interface.id,
            text=self.interface.text,
            style='',
        )

    def create(self):
        pass

    def set_text(self, text):
        pass

    def set_enabled(self, value):
        pass

    def set_background_color(self, value):
        pass

    def set_on_press(self, handler):
        pass

    def rehint(self):
        pass
