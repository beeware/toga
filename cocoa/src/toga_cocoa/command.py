from toga_cocoa.libs import NSMenuItem


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = set()

    def set_enabled(self, value):
        for item in self.native:
            if isinstance(item, NSMenuItem):
                # Menu item enabled status is determined by the app delegate
                item.menu.update()
            else:
                # Otherwise, assume the native object has
                # and explicit enabled property
                item.setEnabled(value)
