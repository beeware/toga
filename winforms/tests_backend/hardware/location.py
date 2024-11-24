from .hardware import HardwareProbe


class LocationProbe(HardwareProbe):
    def cleanup(self):
        pass

    def allow_permissions(self):
        pass

    def allow_permission(self):
        pass

    def grant_permission(self):
        pass

    def reject_permission(self):
        pass

    def add_location(self, loc, *args):
        pass

    def allow_background_permission(self):
        pass
