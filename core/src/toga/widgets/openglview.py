from __future__ import annotations

from typing import Any, Literal, Protocol

from .base import StyleT, Widget


class RendererT(Protocol):
    """A protocol that encapsulates OpenGL rendering operations."""

    def on_init(self, widget: OpenGLView, **kwargs: Any) -> None:
        """The method called when the OpenGLView initializes its content.

        :param widget: The view that is being initialized.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """

    def on_render(
        self, widget: OpenGLView, size: tuple[int, int], **kwargs: Any
    ) -> None:
        """The method called when the OpenGLView needs to re-draw its content.

        :param widget: The view that is being rendered.
        :param size: The size of the current OpenGL viewport.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OpenGLView(Widget):
    def __init__(
        self,
        renderer: RendererT,
        id: str | None = None,
        style: StyleT | None = None,
        **kwargs,
    ):
        """Create a new OpenGLView.

        The widget calls the renderer's `on_init` once when the widget
        implementation is preparing the widget for rendering, and then calls
        the renderer's `on_render` whenever the widget contents need to be
        redrawn.

        This widget makes no assumptions about the OpenGL library that is used to
        perform OpenGL operations.

        :param renderer: The renderer which performs the OpenGL operations.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param kwargs: Initial style properties.
        """
        self._renderer = renderer
        super().__init__(id, style, **kwargs)

    def _create(self):
        return self.factory.OpenGLView(interface=self)

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        OpenGL widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """OpenGLWidgets cannot accept input focus."""
        pass

    def redraw(self) -> None:
        """Flag that the widget needs to be re-rendered."""
        self._impl.redraw()

    @property
    def renderer(self) -> RendererT:
        """The widget's renderer, handling initialization and drawing in OpenGL."""
        return self._renderer
