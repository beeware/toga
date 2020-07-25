
class Command:
    """ Command `native` property is a list of native widgets associated with the command.
    """
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    def set_enabled(self, value):
        pass
        # enabled = self.interface.enabled
        # for widget in self.native:
        #     try:
        #         widget.set_sensitive(enabled)
        #     except AttributeError:
        #         widget.set_enabled(enabled)
