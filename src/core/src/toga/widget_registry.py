class WidgetRegistry:

    def __init__(self):
        self._id_to_widget = {}

    def extend(self, *widgets):
        for widget in widgets:
            self.add(widget)

    def add(self, widget):
        if widget.id in self._id_to_widget:
            # Prevent from adding the same widget twice
            # or adding 2 widgets with the same id
            raise KeyError(
                f'There is already a widget with "{widget.id}" id'
            )
        self._id_to_widget[widget.id] = widget

    def remove(self, id):
        del self._id_to_widget[id]

    def __getitem__(self, id):
        return self._id_to_widget[id]

    def __iter__(self):
        return iter(self._id_to_widget.values())

    def __len__(self):
        return len(self._id_to_widget)

    def __repr__(self):
        return repr(self._id_to_widget)
