# try:
#     import dom
# except ImportError:
#     # The dom module doesn't actually exist; it's a proxy for the browser DOM.
#     # However, if we don't try to import it.
#     pass

from .app import App
from .box import Box
from .button import Button
from .label import Label
from .textinput import TextInput
from .webview import WebView
from .window import Window


# _counter = 1000


# def next_widget_id():
#     global _counter
#     _counter += 1
#     return 'NEW%s' % _counter



def bootstrap_App(element):
    app = App(element.dataset.togaName, element.dataset.togaAppId, element.id[5:])

    element.toga = app
    app.impl = element


def bootstrap_Window(element):
    title = dom.document.title
    content = dom.document.querySelector('[data-toga-parent="' + element.id[5:] + '"]')

    window = Window(element.id[5:], title, content=content)
    element.toga = window
    window.impl = element


def bootstrap_Box(element):
    widget = Box(element.id[5:])

    element.toga = widget
    widget._impl = element


def bootstrap_Label(element):
    widget = Label(element.id[5:], element.innerHTML)

    element.toga = widget
    widget._impl = element


def bootstrap_TextInput(element):
    initial = element.getAttribute('value')
    placeholder = element.getAttribute('placeholder')
    readonly = element.getAttribute('disabled') is not None

    widget = TextInput(element.id[5:], initial, placeholder, readonly)

    element.toga = widget
    widget._impl = element


# def bootstrap_SimpleListElement(element):
#     widget = SimpleListElement(element.id[5:], element.innerHTML, element.dataset.togaDeleteUrl)

#     fn = dom.window.toga.handler(element.dataset.togaOnPress, widget)
#     element.addEventListener('click', fn)

#     element.toga = widget
#     widget._impl = element


# def bootstrap_List(element):
#     children = element.querySelectorAll('[data-toga-parent="' + element.id + '"]')

#     widget = List(element.id[5:], children, element.dataset.togaCreateUrl, element.dataset.togaOnItemPress)

#     element.toga = widget
#     widget._impl = element

def bootstrap_Button(element):
    widget = Button(element.id[5:], element.innerHTML)
    fn = dom.window.toga.handler(element.dataset.togaOnPress, widget)
    element.addEventListener('click', fn)

    element.toga = widget
    widget._impl = element


def bootstrap_WebView(element):
    widget = WebView(element.id[5:])

    element.toga = widget
    widget._impl = element
