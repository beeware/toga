import pytest

from ..probe import BaseProbe


class ScaffoldProbe(BaseProbe):
    def __init__(self, scaffold):
        super().__init__()
        self.window = scaffold.window
        self.scaffold = scaffold
        self.impl = scaffold._impl
        self.container = self.impl.container

    def assert_container_layout(self):
        pass

    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a scaffold container repaint
        self.impl.container.native.displayIfNeeded()

        await super().redraw(message=message, delay=delay, wait_for=wait_for)

    @property
    def content_size(self):
        return (
            self.container.native.frame.size.width,
            self.container.native.frame.size.height,
        )

    async def test_simple_app(self):
        pytest.xfail("Simple apps do not change layout on macOS")
