from toga.interface import ScrollContainer as ScrollContainerInterface

from .base import WidgetMixin
from ..container import Container
from ..libs import *


class ScrollContainer(ScrollContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, horizontal=True, vertical=True, content=None):
        super().__init__(id=None, style=style, horizontal=horizontal, vertical=vertical, content=content)
        self._create()

    def create(self):
        self._impl = NSScrollView.alloc().init()
        self._impl.autohidesScrollers = True
        self._impl.borderType = NSNoBorder
        self._impl.backgroundColor = NSColor.windowBackgroundColor
        # self._impl.backgroundColor = NSColor.blueColor

        # Disable all autolayout functionality on the outer widget
        self._impl.translatesAutoresizingMaskIntoConstraints = False
        self._impl.autoresizesSubviews = True

        self._inner_container = None

        # Add the layout constraints
        self._add_constraints()

    def _set_content(self, container, widget):
        self._impl.documentView = container._impl

        # Enforce a minimum size based on the content
        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._inner_container._impl, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._inner_container._impl, NSLayoutAttributeLeft,
            1.0, 0
        )
        self._inner_container._impl.addConstraint(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._inner_container._impl, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._inner_container._impl, NSLayoutAttributeTop,
            1.0, 0
        )
        self._inner_container._impl.addConstraint(self._height_constraint)

    def _update_child_layout(self):
        if self._content is not None:
            self._inner_container._update_layout()
            self._width_constraint.constant = self.content.layout.width
            self._height_constraint.constant = self.content.layout.height

    def _set_vertical(self, value):
        self._impl.hasVerticalScroller = value

    def _set_horizontal(self, value):
        self._impl.hasHorizontalScroller = value

    def rehint(self):
        self.style.hint(
            min_height=100,
            min_width=100
        )
