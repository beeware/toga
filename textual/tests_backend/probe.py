import asyncio

import pytest

import toga


class BaseProbe:
    HORIZONTAL_SCALE = 800 // 80
    VERTICAL_SCALE = 600 // 25

    def approx_width(self, width):
        return pytest.approx(width, abs=self.HORIZONTAL_SCALE // 2)

    def approx_height(self, height):
        return pytest.approx(height, abs=self.VERTICAL_SCALE // 2)

    async def wait_for_refresh(self):
        app = toga.App.app._impl.native
        loop = asyncio.get_running_loop()
        refreshed = loop.create_future()

        if app.call_after_refresh(refreshed.set_result, None):
            app.refresh(layout=True)
            await refreshed

    async def redraw(self, message=None, delay=0, wait_for=None):
        if toga.App.app.run_slow or wait_for:
            delay = max(1, delay)

        await asyncio.sleep(0)

        print("Waiting for redraw" if message is None else message)
        if delay or wait_for:
            if toga.App.app.run_slow or wait_for is None:
                await asyncio.sleep(delay)
            else:
                delta = 0.1
                interval = 0.0
                while not wait_for() and interval < delay:
                    await asyncio.sleep(delta)
                    interval += delta

        await self.wait_for_refresh()

    def assert_image_size(self, image_size, size, screen, window=None):
        pytest.skip("Image size assertions are not implemented on Textual.")
