import asyncio

from java import dynamic_proxy

from android import R
from android.view import ViewTreeObserver, WindowManagerGlobal


class LayoutListener(dynamic_proxy(ViewTreeObserver.OnGlobalLayoutListener)):
    def __init__(self):
        super().__init__()
        self.event = asyncio.Event()

    def onGlobalLayout(self):
        self.event.set()


class BaseProbe:
    def __init__(self, app):
        self.app = app
        self.activity = app._impl.native
        self.root_view = self.activity.findViewById(R.id.content)

        self.layout_listener = LayoutListener()
        self.root_view.getViewTreeObserver().addOnGlobalLayoutListener(
            self.layout_listener
        )

        self.window_manager = WindowManagerGlobal.getInstance()
        self.original_window_names = self.window_manager.getViewRootNames()

        self.dpi = self.activity.getResources().getDisplayMetrics().densityDpi
        self.scale_factor = self.dpi / 160

    def __del__(self):
        self.root_view.getViewTreeObserver().removeOnGlobalLayoutListener(
            self.layout_listener
        )

    def find_dialog(self):
        new_windows = [
            name
            for name in self.window_manager.getViewRootNames()
            if name not in self.original_window_names
        ]
        if len(new_windows) == 0:
            return None
        elif len(new_windows) == 1:
            return self.window_manager.getRootView(new_windows[0])
        else:
            raise RuntimeError(f"More than one new window: {new_windows}")

    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        self.root_view.requestLayout()
        try:
            event = self.layout_listener.event
            event.clear()
            await asyncio.wait_for(event.wait(), 5)
        except asyncio.TimeoutError:
            print("Redraw timed out")

        if self.app.run_slow:
            delay = min(delay, 1)
        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)
