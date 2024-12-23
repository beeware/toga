__all__ = ["import_module"]


def import_module(name):
    # Pass a dummy `from` list so __import__ will return the actual module rather than
    # the top-level package.
    return __import__(name, {}, {}, ["dummy"])
