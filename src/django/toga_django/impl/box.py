

class Box:
    def __init__(self, id, ports=None):
        self.id = id

        self.children = []

        self.ports = ports if ports else {}

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __html__(self):
        lines = [
            '<div id="toga:%s" data-toga-class="toga.Box" data-toga-parent="%s" data-toga-ports="%s" class="container">' % (
                self.id,
                self.parent.id,
                ",".join(
                    "%s=%s" % (name, id)
                    for name, id in self.ports.items()
                    ),
                )
        ]
        for child in self.children:
            lines.append(child.__html__())
        lines.append('</div>')
        return '\n'.join(lines)
