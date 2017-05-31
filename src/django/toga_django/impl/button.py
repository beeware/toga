

class Button:
    def __init__(self, id, label, ports=None, on_press=None, style=None):
        self.id = id
        self._impl = None
        self.label = label

        self.ports = ports if ports else {}

        self.on_press = on_press
        self.style = style

    def __html__(self):
        return '<button id="toga:%s" class="toga Button btn btn-default" style="%s" data-toga-class="toga.Button" data-toga-parent="%s" data-toga-ports="%s" data-toga-on-press="%s">%s</button>' % (
            self.id,
            self.style,
            self.parent.id,
            '',  #  self.ports,
            self.on_press,
            self.label
        )
