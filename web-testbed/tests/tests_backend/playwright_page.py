import asyncio
import threading

from playwright.async_api import async_playwright


class BackgroundPage:
    def __init__(self):
        self._init = True
        self._ready = threading.Event()
        self._loop = None
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._ready.wait()

    def eval_js(self, js, *args):
        fut = asyncio.run_coroutine_threadsafe(self._eval(js, *args), self._loop)
        return fut.result()

    async def eval_js_async(self, js, *args):
        fut = asyncio.run_coroutine_threadsafe(self._eval(js, *args), self._loop)
        return await asyncio.wait_for(asyncio.wrap_future(fut))

    def _run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.create_task(self._bootstrap())
        self._loop.run_forever()
        self._loop.close()

    async def _bootstrap(self):
        try:
            self._play = await async_playwright().start()
            self._browser = await self._play.chromium.launch(headless=True)
            self._context = await self._browser.new_context()
            await self._context.add_init_script("window.TOGA_WEB_TESTING = true;")

            self._page = await self._context.new_page()

            await self._page.goto(
                "http://localhost:8080", wait_until="load", timeout=30_000
            )

            await self._page.wait_for_function(
                "() => typeof window.test_cmd === 'function'"
            )

            self._alock = asyncio.Lock()
        except Exception:
            raise
        finally:
            self._alock = asyncio.Lock()
            self._ready.set()

    async def _eval(self, js, *args):
        async with self._alock:
            return await self._page.evaluate(js, *args)

    def run_coro(self, coro_fn, *args, **kwargs):
        async def _runner():
            async with self._alock:
                return await coro_fn(self._page, *args, **kwargs)

        fut = asyncio.run_coroutine_threadsafe(_runner(), self._loop)
        return fut.result()

    async def run_coro_async(self, coro_fn, *args, **kwargs):
        async def _runner():
            async with self._alock:
                return await coro_fn(self._page, *args, **kwargs)

        fut = asyncio.run_coroutine_threadsafe(_runner(), self._loop)
        return await asyncio.wait_for(asyncio.wrap_future(fut))
