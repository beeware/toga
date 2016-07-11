from .libs import *
from .widgets.icon import Icon


class Command(object):
    def __init__(self, action, label=None, tooltip=None, icon=None):
        self.action = action
        self.label = label
        self.tooltip = tooltip
        self.icon = Icon.load(icon)

        self._enabled = True
        self._widgets = []

    @property
    def toolbar_identifier(self):
        return 'toolbarItem-%s' % id(self)

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        for widget in self._widgets:
            widget.setEnabled_(value)


class SpecialCommand(object):
    def __init__(self, toolbar_identifier):
        self._toolbar_identifier = toolbar_identifier
        self.label = None
        self.tooltip = None
        self.icon = None

        self._widgets = []

    @property
    def toolbar_identifier(self):
        return self._toolbar_identifier

    @property
    def enabled(self):
        return True


SEPARATOR = SpecialCommand('NSToolbarSeparatorItem')
SPACER = SpecialCommand('NSToolbarSpaceItem')
EXPANDING_SPACER = SpecialCommand('NSToolbarFlexibleSpaceItem')
