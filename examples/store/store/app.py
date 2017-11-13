import toga
from colosseum import CSS


class StoreApp(toga.App):
    def open_document(self, fileURL):
        pass

    def startup(self):
        self.main_window = toga.MainWindow(self.name, size=(500, 300))
        self.main_window.app = self

        self.key_field = toga.TextInput(placeholder='key', initial='test_key', style=CSS(flex=1, padding=5))
        self.value_field = toga.TextInput(placeholder='value', initial='test_value', style=CSS(flex=1, padding=5))
        key_value_box = toga.Box(children=[self.key_field, self.value_field],
                                 style=CSS(flex_direction='row'))

        set_btn = toga.Button('Set', on_press=self.set_value, style=CSS(flex=1))
        get_btn = toga.Button('Get', on_press=self.get_value, style=CSS(flex=1))
        del_btn = toga.Button('Delete', on_press=self.del_value, style=CSS(flex=1))
        btn_box = toga.Box(children=[set_btn, get_btn, del_btn],
                           style=CSS(flex_direction='row'))

        self.label = toga.Label('Hello World')
        outer_box = toga.Box(children=[key_value_box, btn_box, self.label],
                             style=CSS(flex=1, padding=10, min_width=500, min_height=300))

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def set_value(self, widget):
        self.store.set_item(self.key_field.value, self.value_field.value)

    def get_value(self, widget):
        key = self.key_field.value
        value = self.store.get_item(key)
        self.label.text = 'Key: {} Value: {}'.format(key, value)

    def del_value(self, widget):
        key = self.key_field.value
        self.store.remove_item(key)
        self.label.text = 'Removed key: {}'.format(key)


def main():
    return StoreApp('Store Example', 'org.pybee.store')
