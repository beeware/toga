#from .widgets.icon import Icon

class Command:
    def __init__(self, interface):
        self.interface = interface

        # if self.interface.icon_id:
        #     self.icon = Icon.load(self.interface.icon_id)
        # else:
        #     self.icon = None


# # something about this design doesn't seem right
# SEPARATOR = "toolbar_separator"
# SPACER = "toolbar_spacer"
# EXPANDING_SPACER = "toolbar_expanding_spacer"