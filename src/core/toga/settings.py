from pprint import pprint
import toga

from .platform import get_platform_factory


class Settings:
    def __init__(self, version=None):
        self.factory = get_platform_factory()
        self._impl = self.factory.Settings(interface=self)

        self._app = None
        self.groups = []
        self.version = '0.0.0' if version is None else version

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Settings are already associated with an App")
        self._app = app
        self._impl.set_app(app)

    def show(self):
        self._impl.show(None)

    def add_group(self, group):
        if not isinstance(group, SettingsGroup):
            raise ValueError('{} must be instance of SettingsGroup'.format(group))
        self.groups.append(group)

    @property
    def _normal_form(self):
        settings_in_normal_form = {'settings': {'version': self.version,
                                                'groups': [g._normal_form for g in self.groups]}}
        return settings_in_normal_form

    def save_to_file(self, path=None):
        """save the settings to the default settings place on the system"""
        pass

    def load_from_file(self, path=None):
        """load the settings file from the default place on the system"""
        pass


class SettingsItem:
    valid_types = ['switch', 'slider', 'text_field', 'multi_value', 'radio_group']

    def __init__(self, item_type, label, default=None, on_change=None, key=None):
        self._typ = None
        self._label = None
        self._key = None
        self._on_change = None

        self.typ = item_type
        self.label = label
        self.key = key
        self.default = default
        self.on_change = on_change

        self.__normal_form = {}

    # def __init__(self, item_type, label, key=None, **kwargs):
    #     self.typ = item_type.lower()
    #     self.label = label
    #     self.key = label.lower().replace(' ', '_') if key is None else key
    #     self._normal_form = None
    #
    #     if self.typ == 'switch':
    #         self._normal_form = self.make_switch(**kwargs)
    #     elif self.typ == 'slider':
    #         self._normal_form = self.make_slider(**kwargs)
    #     elif self.typ == 'text_field':
    #         self._normal_form = self.make_text_field(**kwargs)
    #     elif self.typ == 'multi_value':
    #         self._normal_form = self.make_multi_value(**kwargs)
    #     elif self.typ == 'radio_group':
    #         self._normal_form = self.make_radio_group(**kwargs)

    @property
    def typ(self):
        return self._typ

    @typ.setter
    def typ(self, typ):
        if typ in self.valid_types:
            self._typ = typ

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label
        else:
            raise ValueError('Label must be of type str.')

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        if key:
            self._key = key
        else:
            self._key = '{label}_{id}'.format(label=self.label.lower().replace(' ', '_'),
                                              id=id(self))

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = handler

    @classmethod
    def Switch(cls, label, default=None, on_change=None, key=None):
        return cls('switch', label, default=default, on_change=on_change, key=key)

    @property
    def _normal_form(self):
        normal_form = {
            'type': self.typ,
            'label': self.label,
            'key': self.key,
            'default': self.default,
            'on_change': self.on_change
        }

        self.__normal_form.update(normal_form)
        return self.__normal_form

    def __repr__(self):
        return str(self._normal_form)

        # def make_switch(self, **kwargs):
        #     required_keys = ['default', 'on_change']
        #     for key in required_keys:
        #         if key not in kwargs.keys():
        #             raise KeyError('Switch is missing "{}" kwarg'.format(key))
        #         if not isinstance(kwargs['default'], bool):
        #             raise Exception('default must be of type bool')
        #         if not callable(kwargs['on_change']):
        #             raise Exception('on_change must be a function')
        #     else:
        #         return {'type': 'switch',
        #                 'label': self.label,
        #                 'key': self.key,
        #                 'default': kwargs['default'],
        #                 'on_change': kwargs['on_change']}

        # def make_slider(self, **kwargs):
        #     required_keys = ['default', 'on_change', 'min', 'max']
        #     for key in required_keys:
        #         if key not in kwargs.keys():
        #             raise KeyError('slider is missing "{}" kwarg'.format(key))
        #         if not callable(kwargs['on_change']):
        #             raise Exception('on_change must be a function')
        #     else:
        #         return {'type': 'slider',
        #                 'label': self.label,
        #                 'key': self.key,
        #                 'default': kwargs['default'],
        #                 'min': kwargs['min'],
        #                 'max': kwargs['max'],
        #                 'on_change': kwargs['on_change']}
        #
        # def make_text_field(self, **kwargs):
        #     required_keys = ['default', 'on_change', 'min', 'max']
        #     pass
        #
        # def make_multi_value(self, **kwargs):
        #     pass
        #
        # def make_radio_group(self, **kwargs):
        #     required_keys = ['default', 'options', 'sorted']
        #     for key in required_keys:
        #         if key not in kwargs.keys():
        #             raise KeyError('{} is missing "{}" kwarg'.format(self.typ, key))
        #     else:
        #         return {'type': 'radio_group', 'label': self.label, 'key': self.key,
        #                 'default': kwargs['default'], 'on_change': kwargs['on_change'],
        #                 'options': kwargs['options'],
        #                 'sorted': kwargs['sorted']}


class SettingsGroup:
    """ The SettingsGroup is a container class for SettingsItems.
    The added SettingsItems are going to be displayed under the
    title and icon of their SettingsGroup.
    """

    def __init__(self, title, items=None, icon=None):
        self.title = title
        self.icon = None if icon is None else icon
        self._items = []
        if items:
            self.items = items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        for item in items:
            if not isinstance(item, SettingsItem):
                raise Exception('Item: {} is not instance of SettingsItem'.format(item))
            self._items.append(item)

    @property
    def _normal_form(self):
        settings_items_in_normal_form = []
        for item in self.items:
            settings_items_in_normal_form.append(item._normal_form)
        normal_form_of_this_group = {'group':
                                         {'title': self.title,
                                          'items': settings_items_in_normal_form}
                                     }
        return normal_form_of_this_group
