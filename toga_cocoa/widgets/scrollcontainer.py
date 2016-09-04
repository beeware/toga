from ..libs import *
from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, horizontal=True, vertical=True, style=None):
        super(ScrollContainer, self).__init__(style=style)
        self.horizontal = horizontal
        self.vertical = vertical

        self._content = None

        self.startup()

    def startup(self):
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(self.vertical)
        self._impl.setHasHorizontalScroller_(self.horizontal)
        self._impl.setAutohidesScrollers_(True)
        self._impl.setBorderType_(NSNoBorder)

        # self._impl.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        # Disable all autolayout functionality
        # self._impl.setAutoresizesSubviews_(False)

        # Also disable autolayout on the clip view.
        # self._impl.contentView.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self._impl.contentView.setAutoresizesSubviews_(False)

        self._impl.setBackgroundColor_(NSColor.windowBackgroundColor())

        # Add the layout constraints
        self._add_constraints()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self.window
        self._content.app = self.app
        self._impl.setDocumentView_(self._content._impl)

    def _set_app(self, app):
        if self._content:
            self._content.app = self.app

    def _set_window(self, window):
        if self._content:
            self._content.window = self.window

    def _apply_layout(self):
        print("SET SCROLL CONTAINER FRAME", self, self.style.layout, self.content.style.layout)
        # content_frame = NSRect(
        #     NSPoint(self.style.layout.left, self.style.layout.top),
        #     NSSize(self.style.layout.width, self.style.layout.height)
        # )
        # self._impl.contentView.setFrame_(content_frame)

        # doc_rect = NSRect(
        #     NSPoint(self._content.style.layout.left, self._content.style.layout.top),
        #     NSSize(self._content.style.layout.width, self._content.style.layout.height)
        # )
        # print("SET BOUNDS")
        # self._content._impl.bounds = doc_rect
        # print("BOUNDS SET")
        self._constraints.update()

        print("SELF", (self._impl.frame.size.width, self._impl.frame.size.height), (self._impl.frame.origin.x, self._impl.frame.origin.y))
        print("CONTENT", (self._impl.contentView.frame.size.width, self._impl.contentView.frame.size.height), (self._impl.contentView.frame.origin.x, self._impl.contentView.frame.origin.y))
        print("DOC", (self._impl.documentView.frame.size.width, self._impl.documentView.frame.size.height), (self._impl.documentView.frame.origin.x, self._impl.documentView.frame.origin.y))

    # def _update_child_layout(self, **style):
    #     """Force a layout update on the children of the scroll container.

    #     The update request can be accompanied by additional style information
    #     (probably min_width, min_height, width or height) to control the
    #     layout.
    #     """
    #     print ('    content:', (self.content._impl.frame.size.width, self.content._impl.frame.size.height), (self.content._impl.frame.origin.x, self.content._impl.frame.origin.y))

    #     # Pass the update request through to the content. Along the way, any
    #     # hard width/height constraints get turned into min width/height
    #     # constraints in the axes where scrolling is allowed.
    #     child_style = {}
    #     for key, value in style.items():
    #         if key == 'width':
    #             if self.horizontal:
    #                 child_style['min_width'] = value
    #             else:
    #                 child_style[key] = value
    #         elif key == 'height':
    #             if self.vertical:
    #                 child_style['min_height'] = value
    #             else:
    #                 child_style[key] = value
    #         else:
    #             child_style[key] = value

    #     print("CHILD STYLE", child_style)
    #     self._content._update_layout(**child_style)
    #     self._content._apply_layout()

    def _update_child_layout(self):
        print("UPDATE CHILD LAYOUT - scrollcontainer")
        if self._content is not None:
            self._content._update_layout()
