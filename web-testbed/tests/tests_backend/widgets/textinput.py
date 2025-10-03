from .base import SimpleProbe

class TextInputProbe(SimpleProbe):
    def __init__(self, widget):
        super().__init__(widget)
        self.widget = widget
        self._last_remote_value = self._read_remote_value()

    def _read_remote_value(self) -> str:
        return self.widget._eval_and_return(f"{self.widget.js_ref}.value")

    @property
    def value(self):
        page = self._page() 
        def _run(p):
            async def steps():
                root = p.locator(f"#{self.dom_id}")
                inner = root.locator("input,textarea").first
                target = inner if (await inner.count()) > 0 else root
                return await target.input_value()
            return steps()
        return page.run_coro(_run)

    @property
    def value_hidden(self) -> bool:
        page = self._page()

        def _run(p):
            async def steps():
                root = p.locator(f"#{self.dom_id}")
                inner = root.locator("input,textarea").first
                target = inner if (await inner.count()) > 0 else root

                # Native password inputs
                t = await target.get_attribute("type")
                if (t or "").lower() == "password":
                    return True
            return steps()

        return bool(page.run_coro(_run))

    
    async def type_character(self, ch: str):
        page = self._page()

        def _run(p):
            async def steps():
                root = p.locator(f"#{self.dom_id}")
                target = (await root.locator("input,textarea").first.count()) and root.locator("input,textarea").first or root
                try: await target.focus()
                except Exception: pass

                if ch == "\n":
                    await target.press("Enter")
                elif ch == "<esc>":
                    await target.press("Escape")
                elif ch in ("<backspace>", "\b"):
                    await target.press("Backspace")
                else:
                    await target.type(ch)
            return steps()

        page.run_coro(_run)

    async def undo(self):
        page = self._page()
        page.run_coro(lambda p: p.locator(f"#{self.dom_id}").press("Control+Z"))

    
    async def redo(self):
        page = self._page()
        page.run_coro(lambda p: p.locator(f"#{self.dom_id}").press("Control+Y"))
    
    def set_cursor_at_end(self):
        page = self._page()
        page.run_coro(
            lambda p: p.evaluate(
                """(sel) => {
                    const root = document.querySelector(sel);
                    if (!root) return;
                    const el = root.matches('input,textarea') ? root : root.querySelector('input,textarea');
                    if (!el) return;
                    el.focus();
                    const len = (el.value ?? '').length;
                    if (typeof el.setSelectionRange === 'function') {
                        el.setSelectionRange(len, len);
                    }
                }""",
                f"#{self.dom_id}",
            )
        )

    async def redraw(self, _msg: str = ""):
        # allow a tick
        page = self._page()
        page.run_coro(lambda p: p.wait_for_timeout(0))
        self._last_remote_value = self._read_remote_value()


