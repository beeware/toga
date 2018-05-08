from toga_dummy.utils import LoggedObject


class Command(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface        
