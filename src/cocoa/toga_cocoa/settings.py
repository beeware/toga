from pprint import pprint
from rubicon.objc import objc_method, NSObject, SEL

import toga
from colosseum import CSS


class SettingsDelegate(NSObject):
    @objc_method
    def openPreferences_(self, interface) -> None:
        print('In Pref')


class Settings:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.window = None
        self.app = None
        self.delegate = SettingsDelegate.alloc().init()
        self.delegate.interface = self

    def set_app(self, app):
        self.app = app

    def show(self, widget):
        print('Open Settings Window.')
        if self.window is None:
            self.window = toga.Window(title='Settings',
                                      position=(150, 150),
                                      size=(540, 380),
                                      minimizable=False,
                                      main_window=False)
            content = self.build_ui_form_normal_form()
            self.window.content = content
        if self.window._impl.native.isVisible:
            self.window._impl.native.makeKeyAndOrderFront_(None)
        else:
            self.window.show()

    def build_ui_form_normal_form(self):
        normal_form = self.interface._normal_form
        # pprint(normal_form)

        version = normal_form['settings']['version']
        groups = normal_form['settings']['groups']

        # if it is more than one group use a option container.
        if len(groups) > 1:
            container = toga.OptionContainer()
        else:
            container = toga.Box(style=CSS(padding=20))

        # iterate over the items in the group and attache them.
        for group in groups:
            group_title = group['group']['title']
            group_items = group['group']['items']

            box = toga.Box()
            # iterate over all items of the group.
            for item in group_items:
                type = item['type']
                label = item['label']
                default = item['default']

                if item['type'] == 'switch':
                    box.add(toga.Switch(label, is_on=default))
            if len(groups) > 1:
                container.add(group_title, box)
            else:
                container.add(box)

        # return the content
        return container
