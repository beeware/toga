class WidgetRegistry(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        # We do not want to allow setting items directly but to use the "add"
        # method instead.
        raise RuntimeError(
            "WidgetRegistry does not allow using item settings directly"
        )

    def extend(self, *widgets):
        for widget in widgets:
            self.add(widget)

    def add(self, widget):
        if widget.id in self:
            # Prevent from adding the same widget twice
            # or adding 2 widgets with the same id
            raise KeyError(
                f'There is already a widget with "{widget.id}" id'
            )
        super().__setitem__(widget.id, widget)

    def remove(self, id):
        del self[id]

    def __iter__(self):
        return iter(self.values())
