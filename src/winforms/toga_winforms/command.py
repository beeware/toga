#from .widgets.icon import Icon

class Command(object):
    def __init__(self, action, label=None, tooltip=None, icon=None):
        self.action = action
        self.label = label
        self.tooltip = tooltip
        #self.icon = Icon.load(icon)

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
            widget.Enabled = value

# something about this design doesn't seem right
SEPARATOR = "toolbar_separator"
SPACER = "toolbar_spacer"
EXPANDING_SPACER = "toolbar_expanding_spacer"