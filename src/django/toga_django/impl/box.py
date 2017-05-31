

class Box:
    def __init__(self, id, style=None):
        self.id = id
        self._impl = None

        self.style = style
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __html__(self):
        lines = [
            '<div id="toga:%s" class="toga Box" style="%s" data-toga-class="toga.Box" data-toga-parent="%s" data-toga-ports="%s">' % (
                self.id,
                self.style,
                self.parent.id,
                '',  #  self.ports,
            )
        ]
        for child in self.children:
            lines.append(child.__html__())
        lines.append('</div>')
        return '\n'.join(lines)
