import pytest

from toga.style.pack import Pack

from ..utils import ExampleNode, ExampleViewport


def test_deprecated_layout_signature():
    """Calling .layout() with two arguments causes a deprecation warning."""

    node = ExampleNode(name="Old Fogey", style=Pack())
    with pytest.warns(
        DeprecationWarning,
        match=r"\(node, viewport\) signature is deprecated",
    ):
        node.style.layout(node, ExampleViewport(50, 50))
