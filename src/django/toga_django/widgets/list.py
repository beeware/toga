from django.core.urlresolvers import reverse, resolve
from django.utils.html import escape

from .base import Widget
from ..libs import List as TogaList, SimpleListElement as TogaSimpleListElement


class SimpleListElement(Widget):
    def __init__(self, content, detail=None, **style):
        super(SimpleListElement, self).__init__(**style)

        self.content = content
        self.detail = detail

        self.startup()

    def startup(self):
        pass

    def materialize(self):
        return TogaSimpleListElement(
            widget_id=self.widget_id,
            content=escape(self.content),
            delete_url=reverse(self.detail, kwargs={'pk': self.content.id})
        )

    def _set_window(self, window):
        super()._set_window(window)
        if self.on_press:
            self.window.callbacks[(self.widget_id, 'on_press')] = self.on_press


class List(Widget):
    IMPL_CLASS = TogaList

    def __init__(self, source=None, detail=None, item_class=None, on_item_press=None, **style):
        super(List, self).__init__(**style)
        self.source = source
        self.detail = detail
        self.item_class = item_class
        self.on_item_press = on_item_press

        self.children = []

        self.startup()

    def startup(self):
        pass

    def materialize(self):
        children = []
        if self.source:
            api_view = resolve(reverse(self.source)).func
            for child in api_view.view_class().get_queryset():
                children.append(self.item_class(child, self.detail).materialize())
        else:
            for child in self.children:
                children.add(child.materialize())

        return TogaList(
            widget_id=self.widget_id,
            children=children,
            create_url=reverse(self.source),
            on_item_press=self.handler(self.on_item_press, 'on_item_press') if self.on_item_press else None
        )

    def add(self, content):
        if self.source:
            raise Exception("Can't manually add to an API-sourced list")
        self.children.append(self.item_class(content, self.detail))

    def _set_app(self, app):
        for child in self.children:
            child.app = app

    def _set_window(self, window):
        for child in self.children:
            child.window = window

        if self.on_item_press:
            self.window.callbacks[(self.widget_id, 'on_item_press')] = self.on_item_press

    # def _hint_size(self, width, height, min_width=None, min_height=None):
    #     if width is not None:
    #         self.width = width
    #     else:
    #         del(self.width)

    #     if min_width is not None:
    #         self.min_width = min_width
    #     else:
    #         del(self.min_width)

    #     if height is not None:
    #         self.height = height
    #     else:
    #         del(self.height)

    #     if min_height is not None:
    #         self.min_height = min_height
    #     else:
    #         del(self.min_height)

    # def _update_child_layout(self, **style):
    #     """Force a layout update on children of this container.

    #     The update request can be accompanied by additional style information
    #     (probably min_width, min_height, width or height) to control the
    #     layout.
    #     """
    #     for child in self.children:
    #         if child.is_container:
    #             child._update_layout()

    # def _set_frame(self, frame):
    #     print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
    #     self._impl.setFrame_(frame)
    #     self._impl.setNeedsDisplay_(True)
    #     for child in self.children:
    #         layout = child.layout
    #         child._set_frame(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))
