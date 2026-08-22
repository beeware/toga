from rubicon.objc import ObjCClass
from tests.conftest import approx

from ..probe import BaseProbe

CATransaction = ObjCClass("CATransaction")


class ScaffoldProbe(BaseProbe):
    def __init__(self, scaffold):
        super().__init__()
        self.window = scaffold.window
        self.scaffold = scaffold
        self.impl = scaffold._impl
        self.container = self.impl.container
        self.nav_controller = self.impl.nav_controller

    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a widget repaint
        self.container.native.layer.displayIfNeeded()

        # Flush CoreAnimation; this ensures all animations are complete
        # and all constraints have been evaluated.
        CATransaction.flush()

        await super().redraw(message=message, delay=delay, wait_for=wait_for)

    async def wait_for_layout(self):
        await self._wait_for_assertion(self.assert_container_layout)

    def assert_container_layout(self):
        # If the window has been laid out, the origin should be the position of the top
        # bar plus the margin.
        assert self.container.content.native.frame.origin.y == approx(
            self.top_bar_height + self.container.content.margin_top
        )
        # Content should be fully laid out and expanded
        assert self.container.content.native.frame.size.width > 0
        assert self.container.content.native.frame.size.height > 0
        assert self.container.content.interface.layout.width > 0
        assert self.container.content.interface.layout.height > 0

    @property
    def top_bar_height(self):
        # On iPadOS multiwindow this can be different, but that can't be tested
        # in testbed unelss we make user drag the window while test is running
        if self.impl.navigation_bar_hidden:
            status_bar_manager = self.window._impl.native.windowScene.statusBarManager
            return status_bar_manager.statusBarFrame.size.height
        else:
            return (
                self.nav_controller.navigationBar.frame.origin.y
                + self.nav_controller.navigationBar.frame.size.height
            )

    @property
    def content_size(self):
        # As a test, assert that our content is not overlapping the top bar.
        self.assert_container_layout()

        # Size does not include bars.
        return (
            self.nav_controller.view.frame.size.width,
            self.nav_controller.view.frame.size.height
            - (
                self.nav_controller.navigationBar.frame.origin.y
                + self.nav_controller.navigationBar.frame.size.height
            ),
        )

    async def test_simple_app(self):
        # Layout remains consistent when navigation bar is hide or shown
        # (this simulates a simple app)
        self.impl.navigation_bar_hiddeen = True
        await self.wait_for_layout()
        self.assert_container_layout()
        self.impl.navigation_bar_hidden = False
        await self.wait_for_layout()
        self.assert_container_layout()
