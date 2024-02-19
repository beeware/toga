import asyncio

from android import R
from android.view import View, ViewTreeObserver, WindowManagerGlobal
from android.widget import Button
from java import dynamic_proxy
from org.beeware.android import MainActivity
from pytest import approx


class LayoutListener(dynamic_proxy(ViewTreeObserver.OnGlobalLayoutListener)):
    def __init__(self):
        super().__init__()
        self.event = asyncio.Event()

    def onGlobalLayout(self):
        self.event.set()


class BaseProbe:
    def __init__(self, app):
        self.app = app
        activity = MainActivity.singletonThis
        self.root_view = activity.findViewById(R.id.content)

        self.layout_listener = LayoutListener()
        self.root_view.getViewTreeObserver().addOnGlobalLayoutListener(
            self.layout_listener
        )

        self.window_manager = WindowManagerGlobal.getInstance()
        self.original_window_names = self.window_manager.getViewRootNames()

        self.dpi = activity.getResources().getDisplayMetrics().densityDpi
        self.scale_factor = self.dpi / 160

    def __del__(self):
        self.root_view.getViewTreeObserver().removeOnGlobalLayoutListener(
            self.layout_listener
        )

    def get_dialog_view(self):
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

    def get_dialog_buttons(self, dialog_view):
        button_panel = dialog_view.findViewById(R.id.button1).getParent()
        return [
            child
            for i in range(button_panel.getChildCount())
            if (
                isinstance(child := button_panel.getChildAt(i), Button)
                and child.getVisibility() == View.VISIBLE
            )
        ]

    def assert_dialog_buttons(self, dialog_view, captions):
        assert [
            str(b.getText()) for b in self.get_dialog_buttons(dialog_view)
        ] == captions

    async def press_dialog_button(self, dialog_view, caption):
        for b in self.get_dialog_buttons(dialog_view):
            if str(b.getText()) == caption:
                b.performClick()
                await self.redraw(f"Click dialog button '{caption}'")
                assert self.get_dialog_view() is None
                break
        else:
            raise ValueError(f"Couldn't find dialog button '{caption}'")

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
            delay = max(delay, 1)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        # Sizes are approximate because of scaling inconsistencies.
        assert image_size == (
            approx(size[0] * self.scale_factor, abs=2),
            approx(size[1] * self.scale_factor, abs=2),
        )
