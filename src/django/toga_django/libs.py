
_counter = 1000


def next_widget_id():
    global _counter
    _counter += 1
    return 'NEW%s' % _counter


class App:
    def __init__(self, name, app_id, ports=None):
        self.name = name
        self.app_id = app_id
        self.widget_id = app_id
        self.main_window = None
        self.windows = []
        self.ports = ports if ports else {}

    def __html__(self):
        return """
        <body id="%s" data-toga-class="toga.App" data-toga-ports="%s" data-toga-app-id="%s" data-toga-name="%s">
        """ % (
            self.widget_id,
            ",".join(
                "%s=%s" % (name, widget_id)
                for name, widget_id in self.ports.items()
            ),
            self.app_id,
            self.name,
        )


def bootstrap_App(element):
    app = App(element.dataset.togaName, element.dataset.togaAppId)

    element.toga = app
    app.impl = element


class Window:
    def __init__(self, widget_id, title, content, ports=None):
        self.widget_id = widget_id

        self.title = title
        self.content = content
        self.content.parent = self

        self.ports = ports if ports else {}


    def __html__(self):
        return """
            <nav id="%s" data-toga-class="toga.Window" data-toga-ports="%s" class="navbar navbar-fixed-top navbar-dark bg-inverse">
                <a class="navbar-brand" href="#">%s</a>
                <ul class="nav navbar-nav">
                    <!--li class="nav-item active">
                      <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                    </li-->
                    <li class="nav-item active">
                      <a class="nav-link" href="https://github.com/freakboy3742/toga_web_demo">Code</a>
                    </li>
                </ul>
            </nav>""" % (
                self.widget_id,
                ",".join(
                    "%s=%s" % (name, widget_id)
                    for name, widget_id in self.ports.items()
                ),
                self.title
            ) + self.content.__html__()


def bootstrap_Window(element):
    title = dom.document.title
    content = dom.document.querySelector('[data-toga-parent="' + element.id + '"]')
    window = Window(element.id, title, content)

    element.toga = window
    window.impl = element


class Container:
    def __init__(self, widget_id, children, ports=None):
        self.widget_id = widget_id

        self.children = children

        for child in children:
            child.parent = self

        self.ports = ports if ports else {}

    def __html__(self):
        lines = ['<div id="%s" data-toga-class="toga.Container" data-toga-parent="%s" data-toga-ports="%s" class="container">' % (
            self.widget_id,
            self.parent.widget_id,
            ",".join(
                "%s=%s" % (name, widget_id)
                for name, widget_id in self.ports.items()
            ),
        )]
        for child in self.children:
            lines.append(child.__html__())
        lines.append('</div>')
        return '\n'.join(lines)


def bootstrap_Container(element):
    children = element.querySelectorAll('[data-toga-parent="' + element.id + '"]')

    widget = Container(element.id, children)

    element.toga = widget
    widget.impl = element


class Button:
    def __init__(self, widget_id, label, ports=None, on_press=None):
        self.widget_id = widget_id

        self.label = label

        self.ports = ports if ports else {}

        self.on_press = on_press

    def __html__(self):
        return '<button id="%s" data-toga-class="toga.Button" data-toga-parent="%s" data-toga-ports="%s" data-toga-on-press="%s">%s</button>' % (
            self.widget_id,
            self.parent.widget_id,
            ",".join(
                "%s=%s" % (name, widget_id)
                for name, widget_id in self.ports.items()
            ),
            self.on_press,
            self.label
        )


def bootstrap_Button(element):
    widget = Button(element.id, element.innerHTML)
    fn = dom.window.toga.handler(element.dataset.togaOnPress, widget)
    element.addEventListener('click', fn)

    element.toga = widget
    widget.impl = element


class SimpleListElement:
    def __init__(self, widget_id, content, delete_url=None, on_press=None, ports=None):
        self.widget_id = widget_id

        self.content = content
        self.delete_url = delete_url
        self.on_press = on_press

        self.ports = ports if ports else {}

    def __html__(self):
        return '<tr id="%s" data-toga-class="toga.SimpleListElement" data-toga-parent="%s" data-toga-ports="%s" data-toga-delete-url="%s" data-toga-on-press="%s"><td>%s</td><td style="width:1em;">%s</td></tr>' % (
            self.widget_id,
            self.parent.widget_id,
            # ",".join(
            #     "%s=%s" % (name, widget_id)
            #     for name, widget_id in self.ports.items()
            # ),
            '',
            self.delete_url if self.delete_url else '',
            self.parent.on_item_press if self.parent.on_item_press else '',
            self.content,
            '<i class="fa fa-times"></i>' if self.delete_url else ''
        )

    def text(self, value):
        self.impl.innerHTML = '<td>%s</td>' % value

    def remove(self):
        self.impl.parentNode.removeChild(self.impl)


def bootstrap_SimpleListElement(element):
    widget = SimpleListElement(element.id, element.innerHTML, element.dataset.togaDeleteUrl)

    fn = dom.window.toga.handler(element.dataset.togaOnPress, widget)
    element.addEventListener('click', fn)

    element.toga = widget
    widget.impl = element


class List:
    def __init__(self, widget_id, children, create_url, on_item_press=None, ports=None):
        self.widget_id = widget_id
        self.create_url = create_url
        self.on_item_press = on_item_press

        self.children = children
        for child in self.children:
            child.parent = self

        self.ports = ports if ports else {}

    def __html__(self):
        lines = [
            '<table id="%s" data-toga-class="toga.List" data-toga-parent="%s" data-toga-ports="%s" data-toga-create-url="%s" data-toga-on-item-press="%s" class="table table-striped">' % (
                self.widget_id,
                self.parent.widget_id,
                ",".join(
                    "%s=%s" % (name, widget_id)
                    for name, widget_id in self.ports.items()
                ),
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
        widget_id = next_widget_id()
        child = SimpleListElement(widget_id, content, on_press=self.on_item_press)

        child.parent = self
        self.impl.children[0].innerHTML += child.__html__()

        child.impl = dom.document.getElementById(widget_id)

        fn = dom.window.toga.handler(self.on_item_press, child)
        child.impl.addEventListener('click', fn)

        return child

    def add_waiting(self):
        self.add('<i class="fa fa-spinner fa-spin"></i>')


def bootstrap_List(element):
    children = element.querySelectorAll('[data-toga-parent="' + element.id + '"]')

    widget = List(element.id, children, element.dataset.togaCreateUrl, element.dataset.togaOnItemPress)

    element.toga = widget
    widget.impl = element


class TextInput:
    def __init__(self, widget_id, initial, placeholder, readonly, ports=None):
        self.widget_id = widget_id

        self.initial = initial
        self.placeholder = None
        self.readonly = False

        self.ports = ports if ports else {}

    def __html__(self):
        return '<input id="%s" data-toga-class="toga.TextInput" data-toga-parent="%s" data-toga-ports="%s" type="text" value="%s"%s%s>' % (
            self.widget_id,
            self.parent.widget_id,
            ",".join(
                "%s=%s" % (name, widget_id)
                for name, widget_id in self.ports.items()
            ),
            self.initial,
            ' placeholder="%s"' % self.placeholder if self.placeholder else '',
            ' disabled' if self.readonly else '',
        )

    def value(self):
        return self.impl.value

    def clear(self):
        self.impl.value = ''


def bootstrap_TextInput(element):
    initial = element.getAttribute('value')
    placeholder = element.getAttribute('placeholder')
    readonly = bool(element.getAttribute('disabled'))

    widget = TextInput(element.id, initial, placeholder, readonly)

    element.toga = widget
    widget.impl = element
