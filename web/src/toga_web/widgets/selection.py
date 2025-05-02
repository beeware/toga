from toga_web.libs import create_proxy

from .base import Widget

class Selection(Widget):

    def create(self):
        self.native = self._create_native_widget("sl-select")
        self.native.addEventListener("sl-change", create_proxy(self.dom_onchange))
    
    def dom_onchange(self, event):
        self.interface.on_change()
    
    def clear(self):
        while self.native.firstElementChild:
            self.native.removeChild(self.native.firstElementChild)
    
    def insert(self, index, item):
        display_text = self.interface._title_for_item(item)
        option = self._create_native_widget("sl-option")
        option.value = display_text
        option.textContent = display_text

        if index >= len(self.native.children):
            self.native.appendChild(option)
        else:
            self.native.insertBefore(option, self.native.children[index])
    
    def get_selected_index(self):
        for i, option in enumerate(self.native.children):
            if option.value == self.native.value:
                return i
        return None
    
    def select_item(self, index, item):
        display_text = self.interface._title_for_item(item)
        self.native.value = display_text
    
    def rehint(self):
        pass
