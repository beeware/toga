from textual._context import active_app
from textual.widgets import TabbedContent as TextualTabbedContent, TabPane
from travertino.size import at_least

from .base import Scalable, Widget


class TogaTabbedContent(TextualTabbedContent):
    DEFAULT_CSS = (
        TextualTabbedContent.DEFAULT_CSS
        + """
        TogaTabbedContent > ContentSwitcher {
            height: 1fr;
        }

        TogaTabPane {
            width: 100%;
            height: 100%;
        }
        """
    )

    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def compose(self):
        # Toga mounts widgets imperatively, outside Textual's compose context.
        # Keep the app context available for TabbedContent's child widgets and timers.
        active_app.set(self.app)
        yield from super().compose()

    def on_mount(self):
        self.impl.on_native_mounted()

    def on_tabbed_content_tab_activated(
        self,
        event: TextualTabbedContent.TabActivated,
    ):
        if event.tabbed_content is self:
            self.impl.on_tab_activated(event.pane.id)


class TogaTabPane(TabPane):
    def __init__(self, option):
        super().__init__(
            option.text,
            option.content.native,
            id=option.id,
            disabled=not option.enabled,
        )
        self.option = option

    def on_mount(self):
        self.option.install_content()


class OptionPaneContainer(Scalable):
    def __init__(self, native, impl):
        self.native = native
        self.impl = impl
        self._width = None
        self._height = None

    def set_size(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        if self._width is None:
            return self.scale_out_horizontal(self.native.size.width)
        return self._width

    @property
    def height(self):
        if self._height is None:
            return self.scale_out_vertical(self.native.size.height)
        return self._height

    def refreshed(self):
        self.impl.on_content_refreshed()


class MeasurementViewport:
    dpi = None
    width = 0
    height = 0


class Option:
    def __init__(self, impl, id, text, content, enabled=True):
        self.impl = impl
        self.id = id
        self.text = text
        self.content = content
        self.enabled = enabled
        self.mounted = False
        self.pane = TogaTabPane(self)
        self.container = OptionPaneContainer(self.pane, impl)

    def install_content(self):
        if self.content.container is not self.container:
            self.content.container = self.container
            for child in self.content.interface.children:
                child._impl.install(parent=self.content)
        self.refresh_content()

    def uninstall_content(self):
        if self.content.container is self.container:
            self.content.container = None

    def refresh_content(self):
        if self.content.container is self.container:
            self.content.interface.refresh()


class OptionContainer(Widget):
    uses_icons = False
    TAB_BAR_HEIGHT = 1

    def create(self):
        self.native = TogaTabbedContent(self)
        self._options = []
        self._next_option_id = 0
        self._current_index = None
        self._native_operation = None
        self._suppress_select_events = 0
        self._initializing = True
        self._measuring_content = False
        self._refreshing_content_layout = False

    def _new_option_id(self):
        self._next_option_id += 1
        return f"toga-option-{self._next_option_id}"

    def _queue_native_operation(self, operation):
        previous = self._native_operation

        async def run_operation():
            if previous is not None:
                await previous
            await operation()

        self._native_operation = self.interface.app._impl.track_dom_operation(
            run_operation()
        )

    def _ensure_active_app(self):
        if self.interface.app is not None:
            active_app.set(self.interface.app._impl.native)

    async def _add_native_option(self, option, before=None, suppress_select=True):
        if option.mounted:
            return

        self._ensure_active_app()
        if suppress_select:
            self._suppress_select_events += 1
        try:
            await self.native.add_pane(option.pane, before=before)
            option.mounted = True
            if not option.enabled:
                self.native.disable_tab(option.id)
            self._sync_native_current()
        finally:
            if suppress_select:
                self._suppress_select_events -= 1

    async def _remove_native_option(self, option):
        if option.mounted:
            self._ensure_active_app()
            await self.native.remove_pane(option.id)
            option.mounted = False

    def _sync_native_current(self):
        if self._current_index is not None:
            self._ensure_active_app()
            option = self._options[self._current_index]
            if self.native.active != option.id:
                self.native.active = option.id

    def _sync_initial_current(self):
        # TabbedContent doesn't expose public pre-mount mutation APIs; initial tabs are
        # staged on Textual's own pending content fields, then Textual composes them.
        if self._current_index is None:
            self.native._initial = ""
        else:
            self.native._initial = self._options[self._current_index].id

    def _native_is_ready(self):
        return self.native.is_attached and self.interface.app is not None

    def on_native_mounted(self):
        self._sync_native_current()
        self.native.app.call_after_refresh(self.finish_initializing)

    def finish_initializing(self):
        self._initializing = False

    def _index_for_option_id(self, option_id):
        for index, option in enumerate(self._options):
            if option.id == option_id:
                return index
        return None

    def on_tab_activated(self, option_id):
        index = self._index_for_option_id(option_id)
        if index is not None:
            self._current_index = index
            if not self._initializing and not self._suppress_select_events:
                self.interface.on_select()

    def on_content_refreshed(self):
        if (
            self.container is not None
            and not self._measuring_content
            and not self._refreshing_content_layout
        ):
            self.interface.refresh()

    def add_option(self, index, text, widget, icon):
        option = Option(
            impl=self,
            id=self._new_option_id(),
            text=text,
            content=widget,
        )
        self._options.insert(index, option)

        if self._current_index is None:
            self._current_index = 0
        elif index <= self._current_index:
            self._current_index += 1

        if self._native_is_ready():
            before = (
                self._options[index + 1].id if index + 1 < len(self._options) else None
            )
            self._queue_native_operation(
                lambda: self._add_native_option(option, before=before)
            )
        else:
            # See _sync_initial_current(); this is Textual's pending pre-mount
            # pane list.
            self.native._tab_content.insert(index, option.pane)
            option.mounted = True
            self._sync_initial_current()

    def remove_option(self, index):
        option = self._options.pop(index)
        option.uninstall_content()

        if self._current_index is not None and index < self._current_index:
            self._current_index -= 1

        if self._native_is_ready():
            self._queue_native_operation(lambda: self._remove_native_option(option))
        else:
            self.native._tab_content.remove(option.pane)
            option.mounted = False
            self._sync_initial_current()

    def set_option_enabled(self, index, enabled):
        option = self._options[index]
        option.enabled = enabled
        option.pane.disabled = not enabled

        if self._native_is_ready() and option.mounted:
            self._ensure_active_app()
            if enabled:
                self.native.enable_tab(option.id)
            else:
                self.native.disable_tab(option.id)

    def is_option_enabled(self, index):
        return self._options[index].enabled

    def set_option_text(self, index, value):
        option = self._options[index]
        option.text = value
        option.pane._title = option.pane.render_str(value)

        if self._native_is_ready() and option.mounted:
            self.native.get_tab(option.id).label = value

    def get_option_text(self, index):
        return self._options[index].text

    def set_option_icon(self, index, value):
        pass

    def get_option_icon(self, index):
        return None

    def get_current_tab_index(self):
        return self._current_index

    def set_current_tab_index(self, current_tab_index):
        self._current_index = current_tab_index
        if self._native_is_ready():
            self._sync_native_current()
        else:
            self._sync_initial_current()

    def activate_native_tab(self, index):
        self._ensure_active_app()
        self.native.active = self._options[index].id

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        content_height = max(
            0,
            height - self.scale_out_vertical(self.TAB_BAR_HEIGHT),
        )
        self._refreshing_content_layout = True
        try:
            for option in self._options:
                option.container.set_size(width, content_height)
                option.refresh_content()
        finally:
            self._refreshing_content_layout = False

    def _measure_content(self, content):
        self._measuring_content = True
        try:
            content.refresh()
            content.interface.style.layout(MeasurementViewport())
            return (
                content.interface.layout.min_width,
                content.interface.layout.min_height,
            )
        finally:
            self._measuring_content = False

    def rehint(self):
        min_width = self.interface._MIN_WIDTH
        min_height = self.interface._MIN_HEIGHT

        for option in self._options:
            width, height = self._measure_content(option.content)
            min_width = max(min_width, width)
            min_height = max(min_height, height)

        self.interface.intrinsic.width = at_least(self.scale_in_horizontal(min_width))
        self.interface.intrinsic.height = at_least(
            self.scale_in_vertical(min_height) + self.TAB_BAR_HEIGHT
        )
