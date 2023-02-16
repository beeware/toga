class TogaApplicator:
    """Apply styles to a Toga widget."""

    def __init__(self, widget):
        self.widget = widget

    def refresh(self):
        # print("RE-EVALUATE LAYOUT", self.widget)
        self.widget.refresh()

    def set_bounds(self):
        # print("  APPLY LAYOUT", self.widget, self.widget.layout)
        self.widget._impl.set_bounds(
            self.widget.layout.absolute_content_left,
            self.widget.layout.absolute_content_top,
            self.widget.layout.content_width,
            self.widget.layout.content_height,
        )
        for child in self.widget.children:
            if child.applicator:
                child.applicator.set_bounds()

    def set_text_alignment(self, alignment):
        self.widget._impl.set_alignment(alignment)

    def set_hidden(self, hidden):
        self.widget._impl.set_hidden(hidden)

    def set_font(self, font):
        # Changing the font of a widget can make the widget change size,
        # which in turn means we need to do a re-layout
        self.widget._impl.set_font(font)
        self.widget._impl.rehint()
        self.widget.refresh()

    def set_color(self, color):
        self.widget._impl.set_color(color)

    def set_background_color(self, color):
        self.widget._impl.set_background_color(color)
