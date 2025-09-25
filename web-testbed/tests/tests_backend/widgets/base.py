class SimpleProbe:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, widget):
        self.id = widget.id
        self.dom_id = f"toga_{widget.id}"

    async def redraw(self, message=None, delay=0):
        page = self._page()

        # Yield to the event loop so on_press handler runs before assertions
        # (wait_for_timeout(0) is a no-op tick in Playwright)
        print("Waiting for redraw" if message is None else message)
        page.run_coro(lambda p: p.wait_for_timeout(delay))
