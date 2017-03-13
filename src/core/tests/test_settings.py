# import pytest
import unittest
from pprint import pprint

from toga.settings import *


class TestSettingsItemSwitch(unittest.TestCase):
    def _callback(self):
        pass

    def test_switch_with_correct_input(self):
        switch = SettingsItem.Switch('My Switch', on_change=self._callback, default=True)
        key = switch.key
        expected_dict = {'default': True, 'label': 'My Switch', 'type': 'switch',
                         'key': key, 'on_change': self._callback}
        self.assertDictEqual(switch._normal_form, expected_dict)

    # def test_switch_with_missing_kwarg_default(self):
    #     with self.assertRaisesRegex(KeyError, 'default'):
    #         SettingsItem('switch', 'My Switch', on_change=self._callback)
    #
    # def test_switch_with_missing_kwarg_callback(self):
    #     with self.assertRaisesRegex(KeyError, 'on_change'):
    #         SettingsItem('switch', 'My Switch', default=True)
    #
    # def test_switch_with_non_bool_for_default(self):
    #     with self.assertRaisesRegex(Exception, 'must be of type bool'):
    #         SettingsItem('switch', 'My Switch', on_change=self._callback, default=self._callback)
    #
    #     with self.assertRaisesRegex(Exception, 'must be of type bool'):
    #         SettingsItem('switch', 'My Switch', on_change=self._callback, default=1)

@unittest.skip
class TestSettingsItemSlider(unittest.TestCase):
    def _callback(self):
        pass

    def test_slider_with_correct_input(self):
        slider = SettingsItem('slider', 'My Slider', default=5, on_change=self._callback, min=0, max=20)
        self.assertEqual(slider._normal_form,
                         {'default': 5,
                          'label': 'My Slider',
                          'type': 'slider',
                          'key': 'my_slider',
                          'min': 0,
                          'max': 20,
                          'on_change': self._callback})


class TestSettingsGroup(unittest.TestCase):
    def _callback(self):
        pass

    def setUp(self):
        self.switch = SettingsItem.Switch('My Switch', on_change=self._callback, default=True)
        self.test_items = [self.switch]

    def test_init_settings_group(self):
        settings_group = SettingsGroup('Default Title')
        self.assertEqual(settings_group.title, 'Default Title')

    def test_init_settings_group_with_settings_items(self):
        settings_items = self.test_items
        settings_group = SettingsGroup('Default Title', items=settings_items)
        self.assertEqual(settings_group.title, 'Default Title')
        self.assertListEqual(settings_group.items, settings_items)
        print(settings_items)
        print(settings_group.items)

    def test_settings_group_with_false_settings_items(self):
        settings_items = [self.switch, 'slider']
        with self.assertRaises(Exception):
            s = SettingsGroup('Default Title', items=settings_items)

    def test_settings_group_normal_form(self):
        settings_group = SettingsGroup('Default Title', items=self.test_items)
        normal_form = settings_group._normal_form
        self.assertEqual(len(normal_form['group']['items']), len(self.test_items))


class TestSettings(unittest.TestCase):
    def _callback(self):
        pass

    def setUp(self):
        self.switch = SettingsItem('switch', 'My Switch', on_change=self._callback, default=True)
        self.switch2 = SettingsItem('switch', 'Switch Two', on_change=self._callback, default=False)
        # self.slider = SettingsItem('slider', 'My Slider', default=5, on_change=self._callback, min=0, max=20)
        self.test_items = [self.switch, self.switch2]
        self.settings_group = SettingsGroup('Test title', self.test_items)

    def test_settings_add_group(self):
        settings = Settings()
        settings.add_group(self.settings_group)
        self.assertListEqual(settings.groups, [self.settings_group])

    def test_settings_add_invalid_group(self):
        settings = Settings()
        with self.assertRaisesRegex(Exception, 'must be instance of SettingsGroup'):
            settings.add_group('Not a Settings Group')

    def test_settings_add_multiple_groups(self):
        settings = Settings()
        group_1 = SettingsGroup('Test title', self.test_items)
        group_2 = SettingsGroup('Test title', self.test_items)
        settings.add_group(group_1)
        settings.add_group(group_2)
        self.assertListEqual(settings.groups, [group_1, group_2])

    def test_settings_get_normal_form(self):
        settings = Settings()
        settings.add_group(self.settings_group)
        pprint(settings._normal_form)
        self.assertIn('settings', settings._normal_form.keys())
        self.assertIn('groups', settings._normal_form['settings'].keys())
