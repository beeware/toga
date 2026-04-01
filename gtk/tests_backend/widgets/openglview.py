from toga.widgets.openglview import LEFT, MIDDLE, RIGHT
from toga_gtk.libs import GTK_VERSION, Gdk, Gtk

from .base import SimpleProbe

BUTTONS = [LEFT, MIDDLE, RIGHT]


class OpenGLViewProbe(SimpleProbe):
    native_class = Gtk.GLArea
    if GTK_VERSION < (4, 0, 0):
        buttons = frozenset({LEFT, MIDDLE, RIGHT})
    else:
        # Not supported yet
        buttons = frozenset()

    if GTK_VERSION < (4, 0, 0):

        async def button_state(self, buttons: frozenset, x=0, y=0):
            for button in buttons:
                await self.button_down(button, x, y)

        async def reset_buttons(self, x=0, y=0):
            for button in BUTTONS:
                await self.button_up(button, x, y)
            await self.redraw("Buttons cleared")

        def _emit_event(self, event_type, x, y, button=1, state=0, emit_name=None):
            event = Gdk.Event.new(event_type)
            event.button = button
            event.x = x
            event.y = y
            if event_type == Gdk.EventType.MOTION_NOTIFY:
                state = state | getattr(Gdk.ModifierType, f"BUTTON{button}_MASK")
            event.state = state

            self.native.emit(
                emit_name or event_type.name.lower().replace("_", "-") + "-event", event
            )

        async def button_down(self, button, x, y):
            self._emit_event(
                Gdk.EventType.BUTTON_PRESS,
                x,
                y,
                button=BUTTONS.index(button),
            )

        async def button_up(self, button, x, y):
            self._emit_event(
                Gdk.EventType.BUTTON_RELEASE,
                x,
                y,
                button=BUTTONS.index(button),
            )
