import sys
from functools import lru_cache

@lru_cache(maxsize=8)
def get_platform_factory():
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