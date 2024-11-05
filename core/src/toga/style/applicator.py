import warnings

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


class TogaApplicator:
    """Apply styles to a Toga widget."""

    def __init__(self, widget: None = None):
        if widget is not None:
            warnings.warn(
                "Widget parameter is deprecated. Applicator will be given a reference "
                "to its widget when it is assigned as that widget's applicator.",
                DeprecationWarning,
                stacklevel=2,
            )

    def refresh(self) -> None:
        # print("RE-EVALUATE LAYOUT", self.node)
        self.node.refresh()

    def set_bounds(self) -> None:
        # print("  APPLY LAYOUT", self.node, self.node.layout)
        self.node._impl.set_bounds(
            self.node.layout.absolute_content_left,
            self.node.layout.absolute_content_top,
            self.node.layout.content_width,
            self.node.layout.content_height,
        )
        for child in self.node.children:
            child.applicator.set_bounds()

    def set_text_alignment(self, alignment: str) -> None:
        self.node._impl.set_alignment(alignment)

    def set_hidden(self, hidden: bool) -> None:
        self.node._impl.set_hidden(hidden)
        for child in self.node.children:
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

    def set_font(self, font: object) -> None:
        # Changing the font of a widget can make the widget change size,
        # which in turn means we need to do a re-layout
        self.node._impl.set_font(font)
        self.node.refresh()

    def set_color(self, color: object) -> None:
        self.node._impl.set_color(color)

    def set_background_color(self, color: object) -> None:
        self.node._impl.set_background_color(color)
