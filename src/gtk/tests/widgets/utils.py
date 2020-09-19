class TreeModelListener:
    """ useful to access paths and iterators from signals """
    def __init__(self, store=None):
        self.changed_path = None
        self.changed_it = None
        self.inserted_path = None
        self.inserted_it = None
        self.deleted_path = None
        if store is not None:
            self.connect(store)

    def on_change(self, model, path, it):
        self.changed_path = path
        self.changed_it = it

    def on_inserted(self, model, path, it):
        self.inserted_path = path
        self.inserted_it = it

    def on_deleted(self, model, path):
        self.deleted_path = path

    def connect(self, store):
        store.connect('row-changed', self.on_change)
        store.connect('row-inserted', self.on_inserted)
        store.connect('row-deleted', self.on_deleted)

    def clear(self):
        self.changed_path = None
        self.changed_it = None
        self.inserted_path = None
        self.inserted_it = None
        self.deleted_path = None
