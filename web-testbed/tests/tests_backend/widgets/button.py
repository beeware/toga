import re

from travertino.colors import rgba

from .base import SimpleProbe

_rgb_re = re.compile(r"rgba?\(([^)]+)\)")


def css_to_travertino(css: str):
    if not css or css == "transparent":
        return None
    m = _rgb_re.search(css)
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(",")]
    r, g, b = map(int, parts[:3])
    a = float(parts[3]) if len(parts) == 4 else 1.0
    return rgba(r, g, b, a)


class ButtonProbe(SimpleProbe):
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
                    return cs.backgroundColor;
                }""",
                f"#{self.dom_id}",
            )
        )
        return css_to_travertino(css)
