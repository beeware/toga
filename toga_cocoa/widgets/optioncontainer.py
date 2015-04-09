from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import *
from .base import Widget


class OptionContainer(Widget):
    def __init__(self, **style):
        super(OptionContainer, self).__init__(**style)
        self._content = []

        self.startup()

    def startup(self):
        print("STARTUP OPTION CONTAINER", self.layout)
        self._impl = NSTabView.alloc().init()
        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    def add(self, label, container):
        self._content.append((label, container))
        container.window = self.window

        item = NSTabViewItem.alloc().initWithIdentifier_('%s-Tab-%s' % (id(self), id(container)))
        item.setLabel_(label)
        container.app = self.app

        item.setView_(container._impl)

        self._impl.addTabViewItem_(item)

    def _update_child_layout(self, **style):
        """Force a layout update on the children of this widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for label, content in self._content:
            # print ('    %s frame:' % label, (content._impl.frame.size.width, content._impl.frame.size.height), (content._impl.frame.origin.x, content._impl.frame.origin.y))
            content._update_layout(
                left=self._impl.contentRect().origin.x,
                top=self._impl.contentRect().origin.y,
                width=self._impl.contentRect().size.width,
                height=self._impl.contentRect().size.height
            )
