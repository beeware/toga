from ..page_singleton import BackgroundPage

class ButtonProbe:
    def __init__(self, widget):
        object.__setattr__(self, "id", widget.id)
        object.__setattr__(self, "dom_id", f"toga_{widget.id}")

    def __getattr__(self, name):
        page = BackgroundPage.get()

        match name:
            case "text":
                # was inner_text, but it trims leading/trailing spaces and removes only whitespace.
                return page.run_coro(lambda page: page.locator(f"#{self.dom_id}").text_content())
            case "height":
                box = page.run_coro(lambda page: page.locator(f"#{self.dom_id}").bounding_box())
                return None if box is None else box["height"]
    
        return "No match"
        #raise AttributeError(name)

        """ ALTERNATIVE METHOD - Keep just in case
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




