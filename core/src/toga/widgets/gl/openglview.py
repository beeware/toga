from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
)

from toga.handlers import wrapped_handler

from ..base import StyleT, Widget

if TYPE_CHECKING:
    from .openglcontext import OpenGLContext


class OnRenderHandler(Protocol):
    def __call__(
        self, widget: OpenGLView, context: OpenGLContext, **kwargs: Any
    ) -> None:
        """A handler invoked when the OpenGLView needs to re-draw its content.

        :param widget: The canvas that was resized.
        :param context: The OpenGLContext.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OpenGLView(Widget):
    def __init__(
        self,
        on_render: OnRenderHandler | None,
        id: str | None = None,
        style: StyleT | None = None,
        **kwargs,
    ):
        self.on_render = None

        super().__init__(id, style, **kwargs)

        self.on_render = on_render

    def _create(self):
        return self.factory.OpenGLView(interface=self)

    def redraw(self):
        self._impl.redraw()

    @property
    def on_render(self) -> OnRenderHandler:
        return self._on_render

    @on_render.setter
    def on_render(self, handler: OnRenderHandler | None):
        self._on_render = wrapped_handler(self, handler)
