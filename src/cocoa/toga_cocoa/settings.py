from pprint import pprint
from rubicon.objc import objc_method, NSObject, SEL
from .libs import *

import toga
from colosseum import CSS


class SettingsDelegate(NSUserDefaultsController):
    @objc_method
    def NSUserDefaultsDidChangeNotification_(self, sender) -> None:
        print('in NSUserDefaultsDidChangeNotification_')
        print(sender)


class Settings:
    """
    Notes:
        When running this as a script all values are saved to ~/Library/Preferences/python.plist
        not as you would expect under ~/Library/Preferences/<Bundle identifier>.plist.
    """

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.window = None
        self.app = None
        self.delegate = SettingsDelegate.alloc().init()
        self.delegate.interface = self
        self.native = NSUserDefaults.standardUserDefaults
        self.native.delegate = SettingsDelegate.alloc().init()
        # print(self.native.dictionaryRepresentation())

    def set_app(self, app):
        self.app = app

    def save_key_value(self, key, value):
        if isinstance(value, bool):
            self.native.setBool_forKey_(value, key)
        elif isinstance(value, int):
            self.native.setInteger_forKey_(value, key)
        elif isinstance(value, float):
            self.native.setDouble_forKey_(value, key)
        else:
            self.native.setObject_forKey_(value, key)

    def set_defaults(self):
        print('Setting defaults:', )
        # store = NSUserDefaults.standardUserDefaults
        normal_form = self.interface._normal_form
        version = normal_form['settings']['version']
        items = normal_form['settings']['items']

        # # set default values
        # key_value_dict = NSMutableDictionary.alloc().init()
        # key_value_dict['version'] = str(version)
        # for item in items:
        #     key_value_dict[item['key']] = str(item['default'])
        # self.native.registerDefaults_(key_value_dict)
        # self.native.synchronize()

        # for item in items:
        #     value = item['default']
        #     key = item['key']
        #     self.save_key_value(key, value)
        #
        # self.native.synchronize()

        # print('for', self.native.objectForKey_('version'))
        # self.native.setObject_forKey_('0.0.7', 'version')
        # self.native.synchronize()
        # print('nach', self.native.objectForKey_('version'))

        for item in items:
            print('Item from store {}: '.format(item['key']), self.native.objectForKey_(item['key']))

        self.native.synchronize()
        pass

    def show(self, widget):
        self.set_defaults()

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
        # print('_-' * 10)
        # pprint(normal_form)

        version = normal_form['settings']['version']
        items = normal_form['settings']['items']

        # get all group names
        groups = []
        for item in items:
            if item['group'] not in groups:
                groups.append(item['group'])

        # if it is more than one group use a option container.
        if len(groups) > 1:
            container = toga.OptionContainer()
        else:
            container = toga.Box(style=CSS(padding=20))

        # iterate over the items in the group and attache them.
        for group in groups:
            # get all items of the group
            group_title = 'Defaults' if group is None else group
            group_items = [item for item in items if item['group'] == group]

            box = toga.Box(style=CSS(padding=20))
            # iterate over all items of the group.
            for item in group_items:
                type = item['type']
                label = item['label']
                default = item['default']
                key = item['key']

                def make_callback(key):
                    def callback(widget):
                        # update the value in settings store
                        self.save_key_value(key, widget.is_on)
                        # call the user defined function for the widget
                        self.interface.callbacks[key](widget)

                    return callback

                print(self.native.boolForKey_(key))

                if type == 'switch':
                    box.add(toga.Switch(label, is_on=bool(self.native.boolForKey_(key)), on_toggle=make_callback(key)))

            if len(groups) > 1:
                container.add(group_title, box)
            else:
                container.add(box)

        # return the content
        return container
