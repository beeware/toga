__all__ = ["version"]


# Return None so it'll work if it's simply assigned in a __version__ attribute, but will
# give an error if it's ever used for anything else.
def version(distribution_name):
    return None
