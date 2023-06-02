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


def _assert_layout(node, expected_layout):
    assert (
        node.layout.absolute_content_left,
        node.layout.absolute_content_top,
    ) == expected_layout["origin"], (
        f"origin of {node} ({node.layout.absolute_content_left},{node.layout.absolute_content_top}) "
        f"doesn't match expected {expected_layout['origin']}"
    )
    assert (node.layout.content_width, node.layout.content_height) == expected_layout[
        "content"
    ], (
        f"content size of {node} ({node.layout.content_width},{node.layout.content_height}) "
        f"doesn't match expected {expected_layout['content']}"
    )

    n_children = len(node.children)
    expected_n_children = len(expected_layout.get("children", []))
    assert n_children == expected_n_children, (
        f"number of children of {node} ({n_children}) "
        f"doesn't match expected {expected_n_children}"
    )

    for child, sublayout in zip(node.children, expected_layout.get("children", [])):
        _assert_layout(child, sublayout)


def assert_layout(node, expected_size, expected_layout):
    """Assert that a node's full recursive layout matches expectation."""
    assert (
        node.layout.width,
        node.layout.height,
    ) == expected_size, (
        f"final size {node.layout.width}x{node.layout.height} "
        f"doesn't match expected {expected_size[0]}x{expected_size[1]}"
    )
    _assert_layout(node, expected_layout)
