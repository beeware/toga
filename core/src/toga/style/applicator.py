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
            child.applicator.set_bounds()

    def set_text_alignment(self, alignment):
        self.widget._impl.set_alignment(alignment)

    def set_hidden(self, hidden):
        self.widget._impl.set_hidden(hidden)
        for child in self.widget.children:
            # If the parent is hidden, then so are all children. However, if the
            # parent is visible, then the child's explicit visibility style is
            # taken into account. This visibility cascades into any
            # grandchildren.
            #
            # parent hidden child hidden style child final hidden state
            # ============= ================== ========================
            # True          True               True
            # True          False              True
            # False         True               True
            # False         False              False
            child.applicator.set_hidden(hidden or child.style._hidden)

    def set_font(self, font):
        # Changing the font of a widget can make the widget change size,
        # which in turn means we need to do a re-layout
        self.widget._impl.set_font(font)
        self.widget.refresh()

    def set_color(self, color):
        self.widget._impl.set_color(color)

    def set_background_color(self, color):
        self.widget._impl.set_background_color(color)
