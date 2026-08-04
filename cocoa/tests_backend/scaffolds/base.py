from ..probe import BaseProbe


class ScaffoldProbe(BaseProbe):
    def __init__(self, scaffold):
        super().__init__()
        self.window = scaffold.window
        self.scaffold = scaffold
        self.impl = scaffold._impl
        self.container = self.impl.container

    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the scaffold, waiting until that redraw has completed."""
        # Force a repaint
        # view = self.impl.root_controller.view
        # view.setNeedsLayout(True)
        # view.layoutSubtreeIfNeeded()
        # view.setNeedsDisplay(True)
        # view.displayIfNeeded()

        await super().redraw(message=message, delay=delay, wait_for=wait_for)

    def assert_container_layout(self):
        pass

    async def wait_for_layout(self):
        # No assertion here by default
        await self.redraw(message="Waiting for scaffold layout to complete")

    @property
    def content_size(self):
        return (
            self.container.native.frame.size.width,
            self.container.native.frame.size.height,
        )
