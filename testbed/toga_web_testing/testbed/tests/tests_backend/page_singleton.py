import asyncio, threading
from playwright.async_api import async_playwright

class BackgroundPage:
    _inst = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._inst is None:
                cls._inst = super().__new__(cls)
        return cls._inst

    @classmethod
    def get(cls):
        return cls()

    def __init__(self):
        if getattr(self, "_init", False):
            return
        self._init = True
        self._ready = threading.Event()
        self._loop = None
        self._thread = threading.Thread(target=self._run, name="PageLoop", daemon=True)
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
            self._page = await self._context.new_page()

            await self._page.goto("http://localhost:8080")
            #await self._page.goto("http://localhost:8080", wait_until="load", timeout=30_000)
            await self._page.wait_for_timeout(5000)

            await self._page.evaluate("(code) => window.test_cmd(code)", "self.my_widgets = {}")

            self._alock = asyncio.Lock()
        except Exception as e:
            self._alock = asyncio.Lock()
        finally:
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