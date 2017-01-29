

class Button:
    def __init__(self, id, label, ports=None, on_press=None):
        self.id = id

        self.label = label

        self.ports = ports if ports else {}

        self.on_press = on_press

    def __html__(self):
        return '<button id="toga:%s" data-toga-class="toga.Button" data-toga-parent="%s" data-toga-ports="%s" data-toga-on-press="%s">%s</button>' % (
            self.id,
            self.parent.id,
            ",".join(
                "%s=%s" % (name, id)
                for name, id in self.ports.items()
            ),
            self.on_press,
            self.label
        )
