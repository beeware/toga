from .base import Widget


class Label(Widget):
    def __html__(self):
        return """
            <span id="toga_{id}" class="toga label" style="{style}">
            {text}
            </span>
        """.format(
            id=self.interface.id,
            text=self.interface.text,
            style=self.interface.style.__css__(),
        )

    def create(self):
        pass

    def set_text(self, text):
        pass

    def set_alignment(self, alignment):
        pass
