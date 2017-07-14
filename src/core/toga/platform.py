import sys
from functools import lru_cache


@lru_cache(maxsize=8)
def get_platform_factory(factory=None):
    """ This function figures out what the current host platform is and
    imports the adequate factory. The factory is the interface to all platform
    specific implementations.

    Args:
        factory (module):

    Returns: The suitable factory for the current host platform
        or the factory that was given as a argument.
    """
    if factory is not None:
        return factory

    if sys.platform == 'ios':
        from toga_iOS import factory
        return factory
    elif sys.platform == 'tvos':
        from toga_tvOS import factory
        return factory
    elif sys.platform == 'watchos':
        from toga_watchOS import factory
        return factory
    elif sys.platform == 'android':
        from toga_android import factory
        return factory
    elif sys.platform == 'darwin':
        from toga_cocoa import factory
        return factory
    elif sys.platform == 'linux':
        from toga_gtk import factory
        return factory
    elif sys.platform == 'win32':
        from toga_win32 import factory
        return factory
    else:
        raise RuntimeError("Couldn't identify a supported host platform.")
