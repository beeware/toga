from js import CustomEvent

from toga_web.libs import create_proxy

from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = self._create_native_widget("wa-select")
        self.native.addEventListener("change", create_proxy(self.dom_change))

    def dom_change(self, event):
        self.interface.on_change()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        while self.native.firstElementChild:
            self.native.removeChild(self.native.firstElementChild)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        display_text = self.interface._title_for_item(item)
        option = self._create_native_widget("wa-option")
        option.value = str(index)
        option.textContent = display_text
        try:
            native_value = self.native.value
        except AttributeError:
            native_value = ""
        if native_value == "":
            self.native.value = option.value
        if index >= len(self.native.children):
            self.native.appendChild(option)
        else:
            self.native.insertBefore(option, self.native.children[index])

    def get_selected_index(self):
        try:
            value = self.native.value
        except AttributeError:
            value = ""
        if value:
            return int(value)
        return None

    def select_item(self, index, item):
        self.native.value = str(index)
        self.native.dispatchEvent(CustomEvent.new("change"))

    def rehint(self):
        pass
