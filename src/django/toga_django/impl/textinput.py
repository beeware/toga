

class TextInput:
    def __init__(self, id, initial, placeholder, readonly, ports=None):
        self.id = id

        self.initial = initial
        self.placeholder = placeholder
        self.readonly = readonly

        self.ports = ports if ports else {}

    def __html__(self):
        return '<input id="toga:%s" data-toga-class="toga.TextInput" data-toga-parent="%s" data-toga-ports="%s" type="text" value="%s"%s%s>' % (
            self.id,
            self.parent.id,
            ",".join(
                "%s=%s" % (name, id)
                for name, id in self.ports.items()
            ),
            self.initial,
            ' placeholder="%s"' % self.placeholder if self.placeholder else '',
            ' disabled' if self.readonly else '',
        )

    def value(self):
        return self.impl.value

    def clear(self):
        self.impl.value = ''
