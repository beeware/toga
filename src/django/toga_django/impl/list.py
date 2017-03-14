
class SimpleListElement:
    def __init__(self, id, content, delete_url=None, on_press=None, style=None):
        self.id = id

        self.content = content
        self.delete_url = delete_url
        self.on_press = on_press
        self.style = style

    def __html__(self):
        return '<tr id="toga:%s" data-toga-class="toga.SimpleListElement" data-toga-parent="%s" data-toga-ports="%s" data-toga-delete-url="%s" data-toga-on-press="%s"><td>%s</td><td style="width:1em;">%s</td></tr>' % (
            self.id,
            self.parent.id,
            '',  #  self.ports,
            self.delete_url if self.delete_url else '',
            self.parent.on_item_press if self.parent.on_item_press else '',
            self.content,
            '<i class="fa fa-times"></i>' if self.delete_url else ''
        )

    def text(self, value):
        self.impl.innerHTML = '<td>%s</td>' % value

    def remove(self):
        self.impl.parentNode.removeChild(self.impl)



class List:
    def __init__(self, id, children, create_url, on_item_press=None):
        self.id = id
        self.create_url = create_url
        self.on_item_press = on_item_press

        self.children = children
        for child in self.children:
            child.parent = self

    def __html__(self):
        lines = [
            '<table id="%s" data-toga-class="toga.List" data-toga-parent="%s" data-toga-ports="%s" data-toga-create-url="%s" data-toga-on-item-press="%s" class="table table-striped">' % (
                self.id,
                self.parent.id,
                '',  # ",".join(
                #     "%s=%s" % (name, id)
                #     for name, id in self.ports.items()
                # ),
                self.create_url,
                self.on_item_press
            )
        ]
        lines.append('<tbody>')
        for child in self.children:
            lines.append(child.__html__())
        lines.append('</tbody>')
        lines.append('</table>')
        return '\n'.join(lines)

    def add(self, content):
        id = next_id()
        child = SimpleListElement(id, content, on_press=self.on_item_press)

        child.parent = self
        self.impl.children[0].innerHTML += child.__html__()

        child.impl = dom.document.getElementById(id)

        fn = dom.window.toga.handler(self.on_item_press, child)
        child.impl.addEventListener('click', fn)

        return child

    def add_waiting(self):
        self.add('<i class="fa fa-spinner fa-spin"></i>')
