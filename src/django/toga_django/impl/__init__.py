# try:
#     import dom
# except ImportError:
#     # The dom module doesn't actually exist; it's a proxy for the browser DOM.
#     # However, if we don't try to import it.
#     pass

from .box import Box
from .button import Button
# from .list import List, SimpleListElement
# from .textinput import TextInput
from .window import Window

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
