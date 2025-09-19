import re


class _ColorLike:
    __slots__ = ("r", "g", "b", "a")

    def __init__(self, r, g, b, a=1.0):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.a = float(a)

    def __repr__(self):
        return f"_ColorLike(r={self.r}, g={self.g}, b={self.b}, a={self.a})"


_CSS_RGBA_RE = re.compile(
    r"rgba?\(\s*(\d+)\s*[, ]\s*(\d+)\s*[, ]\s*(\d+)(?:\s*[/,]\s*([0-9.]+))?\s*\)",
    re.IGNORECASE,
)


def _parse_css_rgba(s: str) -> "_ColorLike | None | str":
    if s is None:
        return None
    s = s.strip().lower()
    # Treat literal 'transparent' as fully transparent black
    if s == "transparent":
        return _ColorLike(0, 0, 0, 0.0)
    m = _CSS_RGBA_RE.match(s)
    if not m:
        # Unknown format, return as-is
        return s
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    a = float(m.group(4)) if m.group(4) is not None else 1.0
    return _ColorLike(r, g, b, a)


class ButtonProbe:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, widget):
        self.id = widget.id
        self.dom_id = f"toga_{widget.id}"

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

        # Click/press
        page.run_coro(lambda p: p.locator(f"#{self.dom_id}").click())

    async def redraw(self, text):
        page = self._page()

        # Yield to the event loop so on_press handler runs before assertions
        # (wait_for_timeout(0) is a no-op tick in Playwright)
        page.run_coro(lambda p: p.wait_for_timeout(0))

    @property
    def background_color(self):
        # Return a Color-like object with .r/.g/.b/.a so the stock assertions
        # (which expect Toga Color objects) work unchanged.

        page = self._page()
        css = page.run_coro(
            lambda p: p.evaluate(
                """(selector) => {
                    const el = document.querySelector(selector);
                    if (!el) return null;
                    const cs = getComputedStyle(el);
                    return cs.backgroundColor; // 'rgb(...)' or 'rgba(...)'
                }""",
                f"#{self.dom_id}",
            )
        )
        return _parse_css_rgba(css)
