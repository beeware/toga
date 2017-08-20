from pprint import pprint
from rubicon.objc import objc_method, NSObject, SEL
from .libs import *

import toga
from colosseum import CSS


class SettingsWindow(toga.Window):
    def on_close(self):
        print('SettingsWindow is about to close.')


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
        self.store = NSUserDefaults.standardUserDefaults
        # print(self.native.dictionaryRepresentation())

    def set_app(self, app):
        self.app = app

    def print_store(self):
        """ debugging method to see what is in the self.store """
        normal_form = self.interface._normal_form
        version = normal_form['settings']['version']
        items = normal_form['settings']['items']
        print('_-' * 10, 'settings store', '-_' * 10)
        print('Settings version: {}'.format(self.store.objectForKey_('version')))
        for item in items:
            print('Key: {}, Value: {}'.format(item['key'], self.store.objectForKey_(item['key'])))
        print('-_' * 25)

    def save_key_value(self, key, value):
        print('save_this: ', value)
        if isinstance(value, bool):
            self.store.setBool_forKey_(value, key)
        elif isinstance(value, int):
            self.store.setInteger_forKey_(value, key)
        elif isinstance(value, float):
            self.store.setDouble_forKey_(value, key)
        elif isinstance(value, list):
            print('save list')
            array = NSMutableArray.alloc().init()
            for item in value:
                print('save value', item)
                array.addObject(NSNumber.numberWithBool(bool(item)))
            else:
                self.store.setObject_forKey_(array, key)
        else:
            self.store.setObject_forKey_(value, key)

    def set_defaults(self):
        """ Sets for every possible key a default value.
        This values are the fallback if no value has been set for a key.

        Notes:
            * This function has to be called every time your app launches,
            macOS does not save defaults to disk.
        """
        normal_form = self.interface._normal_form
        version = normal_form['settings']['version']
        items = normal_form['settings']['items']

        # Create a dict and set the defaults
        key_value_dict = NSMutableDictionary.alloc().init()

        key_value_dict['version'] = str(version)
        for item in items:
            default_value = item['default']
            # if the default_value is a list we have to convert it to a NSArray
            if isinstance(default_value, list):
                array = NSMutableArray.alloc().init()
                for default in default_value:
                    if isinstance(default, bool):
                        array.addObject(NSNumber.numberWithBool(int(default)))
                    if isinstance(default, str):
                        array.addObject(default)
                key_value_dict[item['key']] = array
            else:
                # add default_value to dict
                key_value_dict[item['key']] = str(default_value)
        else:
            NSUserDefaults.standardUserDefaults.registerDefaults_(key_value_dict)
            self.store.synchronize
            self.print_store()

    def show(self, widget):
        self.set_defaults()
        if self.window is None:
            self.window = SettingsWindow(title='Settings',
                                         position=(150, 150),
                                         size=(540, 380),
                                         minimizable=False,
                                         main_window=False)
            self.window._impl.native.releasedWhenClosed = False
            content = self.build_ui_form_normal_form()
            self.window.content = content

        if self.window._impl.native.isVisible:
            self.window._impl.native.makeKeyAndOrderFront_(None)  # Brings the window in
        else:
            self.window.show()

    def build_ui_form_normal_form(self):
        normal_form = self.interface._normal_form
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

            box = toga.Box(style=CSS(padding=15))
            # iterate over all items of the group.
            for item in group_items:
                typ = item['type']
                label = item['label']
                default = item['default']
                key = item['key']

                # Create a callback to update the store value if settings change
                def make_callback(key):
                    def callback(widget):
                        # 1. update the value on disk.
                        if isinstance(widget, toga.Switch):
                            self.save_key_value(key, widget.is_on)
                        elif isinstance(widget, (toga.Slider, toga.Selection, toga.TextInput)):
                            self.save_key_value(key, widget.value)
                        elif isinstance(widget, toga.MultiSelection):
                            print('save this: ', widget.values)
                            self.save_key_value(key, widget.values)
                        else:
                            raise RuntimeError('Unknown widget {}'.format(widget))

                        # 2. invoke the user defined callback.
                        user_def_callback = self.interface.callbacks[key]
                        if user_def_callback is not None:
                            user_def_callback(widget)
                        self.print_store()

                    return callback

                if typ == 'switch':
                    widget = toga.Switch(label, is_on=bool(self.store.boolForKey_(key)), on_toggle=make_callback(key))
                elif typ == 'slider':
                    label = toga.Label(label)
                    slider = toga.Slider(default=float(self.store.doubleForKey_(key)),
                                         range=(item['min'], item['max']),
                                         on_slide=make_callback(key), style=CSS(width=500))
                    widget = toga.Box(children=[label, slider], style=CSS(flex_direction='column'))
                elif typ == 'text_input':
                    label = toga.Label(label, style=CSS(margin_bottom=5))
                    text_input = toga.TextInput(label, initial=self.store.objectForKey_(key),
                                                on_change=make_callback(key),
                                                style=CSS(margin_bottom=10))
                    widget = toga.Box(children=[label, text_input])
                elif typ == 'single_value':
                    label = toga.Label(label, style=CSS(margin_bottom=5))
                    selection = toga.Selection(items=item['choices'], on_select=make_callback(key))
                    selection.value = self.store.stringForKey_(key)
                    widget = toga.Box(children=[label, selection])
                elif typ == 'multi_value':
                    array = self.store.arrayForKey_(key)
                    parsed_defaults = [bool(d.boolValue) for d in list(array)]
                    widget = toga.MultiSelection(label,
                                                 choices=item['choices'],
                                                 defaults=parsed_defaults,
                                                 on_select=make_callback(key))
                box.add(widget)

            if len(groups) > 1:
                box.style.width = 500
                container.add(group_title, box)
            else:
                container.add(box)

        # return the content
        return container
