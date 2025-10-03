from .base import SimpleProbe


class SwitchProbe(SimpleProbe):
    @property
    def text(self):
        page = self._page()
        return page.run_coro(lambda p: p.locator(f"#{self.dom_id}").text_content())

    @property
    def height(self):
        page = self._page()
        box = page.run_coro(lambda p: p.locator(f"#{self.dom_id}").bounding_box())
        return None if box is None else box["height"]

    async def press(self):
        page = self._page()
        page.run_coro(lambda p: p.locator(f"#{self.dom_id}").click())
