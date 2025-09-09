class ButtonProbe:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, widget):
        object.__setattr__(self, "id", widget.id)
        object.__setattr__(self, "dom_id", f"toga_{widget.id}")

    @property
    def text(self):
        page = self._page()
        return page.run_coro(lambda p: p.locator(f"#{self.dom_id}").text_content())

    @property
    def height(self):
        page = self._page()
        box = page.run_coro(lambda p: p.locator(f"#{self.dom_id}").bounding_box())
        return None if box is None else box["height"]

    # Alternate Method (non-lambda)
    """
    sel = f"#{self.dom_id}"

    if name == "text":
        async def _text(page):
            return await page.locator(sel).inner_text()
        return w.run_coro(_text)

    if name == "height":
        async def _height(page):
            box = await page.locator(sel).bounding_box()
            return None if box is None else box["height"]
        return w.run_coro(_height)
    """
