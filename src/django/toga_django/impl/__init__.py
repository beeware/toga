try:
    import dom
except ImportError:
    pass

# from .box import Box


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
            '<div id="%s" data-toga-class="toga.Box" data-toga-parent="%s" data-toga-ports="%s" class="container">' % (
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

# from .button import Button


class Button:
    def __init__(self, id, label, ports=None, on_press=None):
        self.id = id

        self.label = label

        self.ports = ports if ports else {}

        self.on_press = on_press

    def __html__(self):
        return '<button id="%s" data-toga-class="toga.Button" data-toga-parent="%s" data-toga-ports="%s" data-toga-on-press="%s">%s</button>' % (
            self.id,
            self.parent.id,
            ",".join(
                "%s=%s" % (name, id)
                for name, id in self.ports.items()
            ),
            self.on_press,
            self.label
        )

# from .list import List, SimpleListElement
# from .textinput import TextInput
# from .window import Window


class Window:
    def __init__(self, id, title, content=None, ports=None):
        self.id = id

        self.title = title
        self.set_content(content)

        self.ports = ports if ports else {}

    def __html__(self):
        return """
            <nav id="%s" data-toga-class="toga.Window" data-toga-ports="%s" class="navbar navbar-fixed-top navbar-dark bg-inverse">
                <a class="navbar-brand" href="#">%s</a>
                <ul class="nav navbar-nav">
                    <!--li class="nav-item active">
                      <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                    </li-->
                </ul>
            </nav>""" % (
                self.id,
                ",".join(
                    "%s=%s" % (name, id)
                    for name, id in self.ports.items()
                ),
                self.title
            ) + self.content.__html__()

    def set_title(self, title):
        self.title = title
        dom.window.title = title

    def set_content(self, content):
        self.content = content
        if content:
            self.content.parent = self


# _counter = 1000


# def next_widget_id():
#     global _counter
#     _counter += 1
#     return 'NEW%s' % _counter


# def bootstrap_App(element):
#     app = App(element.dataset.togaName, element.dataset.togaAppId)

#     element.toga = app
#     app.impl = element


def bootstrap_Window(element):
    title = dom.document.title
    content = dom.document.querySelector('[data-toga-parent="' + element.id + '"]')
    window = Window(element.id, title, content=content)
    element.toga = window
    window.impl = element


def bootstrap_Box(element):
    widget = Box(element.id)

    element.toga = widget
    widget.impl = element


# def bootstrap_TextInput(element):
#     initial = element.getAttribute('value')
#     placeholder = element.getAttribute('placeholder')
#     readonly = bool(element.getAttribute('disabled'))

#     widget = TextInput(element.id, initial, placeholder, readonly)

#     element.toga = widget
#     widget.impl = element


# def bootstrap_SimpleListElement(element):
#     widget = SimpleListElement(element.id, element.innerHTML, element.dataset.togaDeleteUrl)

#     fn = dom.window.toga.handler(element.dataset.togaOnPress, widget)
#     element.addEventListener('click', fn)

#     element.toga = widget
#     widget.impl = element


# def bootstrap_List(element):
#     children = element.querySelectorAll('[data-toga-parent="' + element.id + '"]')

#     widget = List(element.id, children, element.dataset.togaCreateUrl, element.dataset.togaOnItemPress)

#     element.toga = widget
#     widget.impl = element

def bootstrap_Button(element):
    widget = Button(element.id, element.innerHTML)
    fn = dom.window.toga.handler(element.dataset.togaOnPress, widget)
    element.addEventListener('click', fn)

    element.toga = widget
    widget.impl = element
