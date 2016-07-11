from ..libs import *
from .base import Widget


class TogaSplitViewDelegate(NSObject):
    @objc_method
    def splitView_resizeSubviewsWithOldSize_(self, view, size: NSSize) -> None:
        view.adjustSubviews()

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the window is actually visible, and the split has moved,
        # a resize of all the content panels is required.
        if self.interface.window._impl.isVisible:
            # print ("SPLIT CONTAINER LAYOUT CHILDREN", self.interface._content[0]._impl.frame.size.width, self.interface._content[1]._impl.frame.size.width)
            self.interface._update_child_layout()


class SplitContainer(Widget):
    HORIZONTAL = False
    VERTICAL = True

    def __init__(self, direction=VERTICAL, style=None):
        super(SplitContainer, self).__init__(style=style)
        self.is_container = True
        self._impl = None
        self._content = None
        self._right_content = None

        self.direction = direction

        self.startup()

    def startup(self):
        self._impl = NSSplitView.alloc().init()
        self._impl.setVertical_(self.direction)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(True)

        self._delegate = TogaSplitViewDelegate.alloc().init()
        self._delegate.interface = self

        self._impl.setDelegate_(self._delegate)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if len(content) < 2:
            raise ValueError('SplitContainer content must have at least 2 elements')

        self._content = content

        for cont in self._content:
            cont.window = self.window
            cont.app = self.app
            self._impl.addSubview_(cont._impl)
            cont._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)

    def _set_app(self, app):
        if self._content:
            for content in self._content:
                content.app = self.app

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content.window = self.window

    def _update_child_layout(self, **style):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for i, content in enumerate(self._content):
            frame = content._impl.frame
            content._update_layout(
                left=frame.origin.x,
                top=frame.origin.y,
                width=frame.size.width,
                height=frame.size.height
            )
