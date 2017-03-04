

class TextInput:
    def __init__(self, id, initial, placeholder, readonly, style=None):
        self.id = id

        self.initial = initial
        self.placeholder = placeholder
        self.readonly = readonly
        self.style = style

    def __html__(self):
        return '<input id="toga:%s" class="toga TextInput" style="%s" data-toga-class="toga.TextInput" data-toga-parent="%s" data-toga-ports="%s" type="text" value="%s"%s%s>' % (
            self.id,
            self.style.render(),
            self.parent.id,
            '',  #  self.ports,
            self.initial,
            ' placeholder="%s"' % self.placeholder if self.placeholder else '',
            ' disabled' if self.readonly else '',
        )

    @property
    def value(self):
        return self.impl.value

    @value.setter
    def value(self, value):
        print("value", value)
        self.impl.value = value

    def clear(self):
        self.impl.value = ''
