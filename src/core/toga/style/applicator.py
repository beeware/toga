
class TogaApplicator:
    """Apply styles to Toga widgets"""
    def set_bounds(self, widget):
        # print("LAYOUT", widget, widget._layout)
        widget._impl.set_bounds(
            widget.layout.absolute_content_left, widget.layout.absolute_content_top,
            widget.layout.content_width, widget.layout.content_height
        )
        for child in widget.children:
            self.set_bounds(child)
