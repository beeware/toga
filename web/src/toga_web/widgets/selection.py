from js import CustomEvent

from toga_web.libs import create_proxy

from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-select")
        self.native.addEventListener("sl-change", create_proxy(self.dom_sl_change))

    def dom_sl_change(self, event):
        self.interface.on_change()

    def clear(self):
        while self.native.firstElementChild:
            self.native.removeChild(self.native.firstElementChild)

    def insert(self, index, item):
        display_text = self.interface._title_for_item(item)
        option = self._create_native_widget("sl-option")
        option.value = str(index)
        option.textContent = display_text
        if self.native.value == "":
            self.native.value = option.value
        if index >= len(self.native.children):
            self.native.appendChild(option)
        else:
            self.native.insertBefore(option, self.native.children[index])

    def get_selected_index(self):
        if self.native.value:
            return int(self.native.value)
        return None

    def select_item(self, index, item):
        self.native.value = str(index)
        self.native.dispatchEvent(CustomEvent.new("sl-change"))

    def rehint(self):
        pass
