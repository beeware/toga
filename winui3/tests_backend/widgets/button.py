import asyncio

import pytest
from toga_winui3.libs.nativeevents import NativeEvent
from win32more import unbox_value
from win32more.Microsoft.UI.Xaml.Controls import Button as NativeButton, ImageIcon

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = NativeButton

    def __init__(self, widget):
        super().__init__(widget)

        # Check the Click event is being properly handled.
        assert isinstance(self.native.event_handler.Click, NativeEvent)

    @property
    def content_is_text(self):
        try:
            content = unbox_value(self.native.Content)
            return isinstance(content, str)
        except TypeError:
            return False

    @property
    def text(self):
        if not self.content_is_text:
            return ""

        text = unbox_value(self.native.Content)

        # Normalize the zero width space to the empty string.
        if text == "\u200b":
            return ""
        return text

    def assert_no_icon(self):
        button_content = self.native.Content
        if button_content:
            # Try to cast the Button content as an icon
            image_icon = ImageIcon(value=button_content.value)

            try:
                image_icon.Width  # noqa B018
                pytest.fail("Button has an icon.")
            except OSError:
                # There should be an OSError exception
                pass

    def assert_icon_size(self):
        button_content = self.native.Content
        if button_content:
            # Cast the Button content as an icon
            image_icon = ImageIcon(value=button_content.value)

            assert image_icon.Width == 32
            assert image_icon.Height == 32
        else:
            pytest.fail("Button has no content.")

    async def press(self):
        # A small delay to ensure that the button is added to the visual tree.
        await asyncio.sleep(0.05)
        midpoint = self._midpoint_screen_coords
        await self._send_click(*midpoint)
