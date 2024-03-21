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
        return f"<{self.name}>"

    def __html__(self, depth=0):
        """Debugging helper - output the HTML interpretation of this layout"""
        if depth:
            tag = "div"
        else:
            tag = "body"
        lines = []

        # Add an interpretation of intrinsic width
        extra_style = [""]
        if self.intrinsic.width:
            try:
                extra_style.append(f"min-width: {self.intrinsic.width.value}px;")
            except AttributeError:
                extra_style.append(f"min-width: {self.intrinsic.width}px;")
        if self.intrinsic.height:
            try:
                extra_style.append(f"min-height: {self.intrinsic.height.value}px;")
            except AttributeError:
                extra_style.append(f"min-height: {self.intrinsic.height}px;")
        extra_css = " ".join(extra_style)

        lines.append(
            "    " * (depth + 1)
            + f'<{tag} id="{self.name}" style="{self.style.__css__()}{extra_css}">'
        )
        if self.children:
            for child in self.children:
                lines.append(child.__html__(depth=depth + 1))
            lines.append("    " * (depth + 1) + f"</{tag}>")
        else:
            lines[-1] = lines[-1] + f"</{tag}>"
        return "\n".join(lines)

    def refresh(self):
        # We're directly modifying styles and computing layouts for specific
        # viewports, so we don't need to trigger layout changes when a style is
        # changed.
        pass


class ExampleViewport:
    def __init__(self, width, height):
        self.height = height
        self.width = width


def _assert_layout(node, expected_layout):
    assert (
        node.layout.absolute_content_left,
        node.layout.absolute_content_top,
    ) == expected_layout["origin"], (
        f"origin of {node} ({node.layout.absolute_content_left}, {node.layout.absolute_content_top}) "
        f"doesn't match expected {expected_layout['origin']}"
    )
    assert (node.layout.content_width, node.layout.content_height) == expected_layout[
        "content"
    ], (
        f"content size of {node} ({node.layout.content_width}, {node.layout.content_height}) "
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


def assert_layout(node, min_size, expected_size, expected_layout):
    """Assert that a node's full recursive layout matches expectation."""
    assert (
        node.layout.min_width,
        node.layout.min_height,
    ) == min_size, (
        f"minimum size {node.layout.min_width}x{node.layout.min_height} "
        f"doesn't match expected {min_size[0]}x{min_size[1]}"
    )

    assert (
        node.layout.width,
        node.layout.height,
    ) == expected_size, (
        f"final size {node.layout.width}x{node.layout.height} "
        f"doesn't match expected {expected_size[0]}x{expected_size[1]}"
    )
    _assert_layout(node, expected_layout)
