from unittest.mock import Mock

from travertino.node import Node

from toga.style.applicator import TogaApplicator


class ExampleNode(Node):
    def __init__(self, name, style, size=None, children=None):
        super().__init__(
            style=style, children=children, applicator=TogaApplicator(self)
        )

        self.name = name
        self._impl = Mock()
        if size:
            self.intrinsic.width = size[0]
            self.intrinsic.height = size[1]

        self.refresh = Mock()

    def __repr__(self):
        return f"<{self.name} at {id(self)}>"

    def refresh(self):
        # We're directly modifying styles and computing layouts for specific
        # viewports, so we don't need to trigger layout changes when a style is
        # changed.
        pass


class ExampleViewport:
    def __init__(self, width, height, dpi=96, baseline_dpi=96):
        self.height = height
        self.width = width
        self.dpi = dpi
        self.baseline_dpi = baseline_dpi
