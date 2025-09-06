class ButtonProbe:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, widget):
        object.__setattr__(self, "id", widget.id)
        object.__setattr__(self, "dom_id", f"toga_{widget.id}")

    def __getattr__(self, name):
        page = self._page()

        match name:
            case "text":
                # Was inner_text, but it trims leading/trailing spaces and removes only
                # whitespace.
                return page.run_coro(
                    lambda p: p.locator(f"#{self.dom_id}").text_content()
                )
            case "height":
                box = page.run_coro(
                    lambda p: p.locator(f"#{self.dom_id}").bounding_box()
                )
                return None if box is None else box["height"]

        return "No match"
        # raise AttributeError(name)

        # Alternate Method - Keep just in case
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
