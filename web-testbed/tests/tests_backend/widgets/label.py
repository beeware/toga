from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    def __init__(self, widget):
        super().__init__(widget)
        self._baseline_height = 0

    @property
    def text(self):
        page = self._page()
        return page.run_coro(lambda p: p.locator(f"#{self.dom_id}").text_content())

    @property
    def width(self):
        page = self._page()
        box = page.run_coro(lambda p: p.locator(f"#{self.dom_id}").bounding_box())
        return None if box is None else box["width"]

    @property
    def height(self):
        page = self._page()

        box = page.run_coro(lambda p: p.locator(f"#{self.dom_id}").bounding_box())
        h = 0 if box is None else box["height"]

        text = self.text or ""
        lines = text.count("\n") + 1

        if h > 0 and self._baseline_height == 0:
            self._baseline_height = h
        baseline = self._baseline_height or h or 0

        if text == "":
            return baseline

        if lines > 1 and baseline > 0:
            return baseline * lines

        return h if h > 0 else baseline
