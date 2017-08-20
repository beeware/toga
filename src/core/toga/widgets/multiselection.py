from .base import Widget


class MultiSelection(Widget):
    def __init__(self, label, choices, defaults=None, on_select=None, row=False,
                 id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self.choices = choices
        self.defaults = defaults

        self._impl = self.factory.MultiSelection(interface=self)
        self.label = label
        self.row = row
        self.on_select = on_select

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        if isinstance(value, bool):
            self._row = value
            self._impl.set_row(self._row)


    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = str(label)
        self._impl.set_label(self._label)

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, choices):
        self._choices = choices

    @property
    def defaults(self):
        """ Defaults must be a list of ``bool`` with the same length
        as the provided choices.

        Returns:
            A ``list`` of ``bool``. Every choice has its own default.
        """
        return self._defaults

    @defaults.setter
    def defaults(self, defaults):
        if isinstance(defaults, list) and len(defaults) == len(self.choices):
            self._defaults = defaults

    @property
    def on_select(self):
        return self._on_change

    @on_select.setter
    def on_select(self, handle):
        self._on_change = handle if callable(handle) else None

    @property
    def values(self):
        """
        Returns:
            A ``list`` of all selected items. Empty `[]` if nothing is selected.
        """
        return self._impl.get_selected_items()
