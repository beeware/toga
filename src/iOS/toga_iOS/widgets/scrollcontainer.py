from rubicon.objc import CGSizeMake
from toga_iOS.libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeHeight,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTop,
    NSLayoutAttributeTrailing,
    NSLayoutAttributeWidth,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    UIScrollView
)
from toga_iOS.window import (
    iOSViewport,
    UIColor
)
from travertino.size import at_least
from .base import Widget


class ScrollContainer(Widget):
    __current_content = None
    __scroll_height_constraint = None
    __scroll_width_constraint = None
    __vertical_enabled = False
    __horizontal_enabled = False
    
    def __update_content_size(self):
        # We need a layout pass to figure out how big the scrollable area should be
        self.__current_content.interface.refresh()
        
        content_width = 0
        padding_horizontal = 0
        content_height = 0
        padding_vertical = 0
        
        if self.__horizontal_enabled:
            content_width = self.__current_content.interface.layout.width
            padding_horizontal = self.__current_content.interface.style.padding_left + self.__current_content.interface.style.padding_right
        else:
            content_width = self.native.frame.size.width
        
        if self.__vertical_enabled:
            content_height = self.__current_content.interface.layout.height
            padding_vertical = self.__current_content.interface.style.padding_top + self.__current_content.interface.style.padding_bottom
            # pad the scrollview for the statusbar offset
            padding_vertical = padding_vertical + self.__current_content.viewport.statusbar_height
        else:
            content_height = self.native.frame.size.height

        self.native.setContentSize_(CGSizeMake(content_width + padding_horizontal,
                                               content_height + padding_vertical))

    def __constrain_to_scrollview(self, widget):
        # The scrollview should know the content size as long as the
        # view contained has an intrinsic size and the constraints are
        # not ambiguous in any axis.
        view = widget.native
        horizontal = NSLayoutConstraint.constraintsWithVisualFormat_options_metrics_views_(
            'H:|[view]|',
            0,
            None,
            {'view': view}
        )
        self.native.addConstraints_(horizontal)

        vertical = NSLayoutConstraint.constraintsWithVisualFormat_options_metrics_views_(
            'V:|[view]|',
            0,
            None,
            {'view': view}
        )
        self.native.addConstraints_(vertical)

    def create(self):
        self.native = UIScrollView.alloc().init()
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.backgroundColor = UIColor.whiteColor
        self.add_constraints()

    def set_content(self, widget):
        if self.__current_content != None:
            self.__current_content.removeFromSuperview()
        self.__current_content = widget
        self.native.addSubview(widget.native)
        widget.viewport = iOSViewport(self.native)

        for child in widget.interface.children:
            child._impl.container = widget

        self.__constrain_to_scrollview(widget)

    def set_vertical(self, value):
        self.__vertical_enabled = value
        if self.__current_content:
            self.__update_content_size()

    def set_horizontal(self, value):
        self.__horizontal_enabled = value
        if self.__current_content:
            self.__update_content_size()

    def rehint(self):
        self.__update_content_size()
