

class Label:
    def __init__(self, id, text, alignment=None, ports=None, on_press=None, style=None):
        self.id = id

        self.text = text
        self.style = style

    def __html__(self):
        return '<span id="toga:%s" class="toga Label" style="%s" data-toga-class="toga.Label" data-toga-parent="%s" data-toga-ports="%s">%s</span>' % (
            self.id,
            self.style,
            self.parent.id,
            '',  #  self.ports,
            self.text,
        )
