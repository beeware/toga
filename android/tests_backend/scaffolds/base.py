import asyncio

from android.content import Context

from ..probe import BaseProbe


class ScaffoldProbe(BaseProbe):
    def __init__(self, app, scaffold):
        super().__init__(app)
        self.scaffold = scaffold
        self.impl = scaffold._impl
        self.container = self.impl.container

    async def _wait_for_assertion(self, assertion):
        # Loop for up to `timeout` seconds, until assertion() passes without
        # raising an AssertionError
        timeout = 5
        polling_interval = 0.1
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        while (loop.time() - start_time) < timeout:
            try:
                assertion()
                return
            except AssertionError as e:
                exception = e
                await asyncio.sleep(polling_interval)

        raise exception

    def assert_container_layout(self):
        # The scaffold's container is displayed as the root content view.
        assert self.container.native_parent == self.root_view

        # The navigation bar visibility matches the scaffold's configuration.
        actionbar = self.app._impl.native.getSupportActionBar()
        assert actionbar.isShowing() != self.impl.navigation_bar_hidden

        # The container has been resized to fill the root content view.
        assert self.container.native_width == self.root_view.getWidth()
        assert self.container.native_height == self.root_view.getHeight()

        # Content has been fully laid out.
        assert self.container.content.interface.layout.content_width > 0
        assert self.container.content.interface.layout.content_height > 0

    async def wait_for_layout(self):
        await self._wait_for_assertion(self.assert_container_layout)

    @property
    def top_bar_height(self):
        # Android doesn't require explicit allowances for the top bar in content layout;
        # the size of the top bar is the difference between the screen and the root
        # window content size.
        context = self.app._impl.native.getApplicationContext()
        window_manager = context.getSystemService(Context.WINDOW_SERVICE)
        display = window_manager.getDefaultDisplay()
        return (display.getHeight() - self.root_view.getHeight()) / self.scale_factor

    @property
    def content_size(self):
        return (
            self.root_view.getWidth() / self.scale_factor,
            self.root_view.getHeight() / self.scale_factor,
        )

    async def verify_simple_app(self):
        # Layout remains consistent when the navigation bar is hidden or shown
        # (this simulates a simple app).
        self.impl.navigation_bar_hidden = True
        await self.redraw("Navigation bar hidden")
        await self.wait_for_layout()
        self.impl.navigation_bar_hidden = False
        await self.redraw("Navigation bar shown")
        await self.wait_for_layout()
