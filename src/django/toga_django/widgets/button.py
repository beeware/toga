from .. import impl


class Button(Widget):
    def create(self):
        self._impl = impl.Button(
            id=self.id,
            label=self._config['label'],
            on_press=self.handler(self._config['on_press'], 'on_press') if self._config['on_press'] else None,
            style=self.style,
        )

    def set_window(self, window):
        super()._set_window(window)
        if self.on_press:
            self.window.callbacks[(self.id, 'on_press')] = self.on_press

    def set_label(self, label):
        pass

    def set_enabled(self, value):
        pass

    def set_background_color(self, value):
        pass

    def set_on_press(self, handler):
        pass

    def rehint(self):
        pass
