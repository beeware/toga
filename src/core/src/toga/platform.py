import sys
from functools import lru_cache


# Rely on `sys.getandroidapilevel`, which only exists on Android; see
# https://github.com/beeware/Python-Android-support/issues/8
if hasattr(sys, 'getandroidapilevel'):
    current_platform = 'android'
elif sys.platform == 'emscripten':
    current_platform = 'web'
else:
    current_platform = sys.platform


@lru_cache(maxsize=8)
def get_platform_factory(factory=None):
    """ This function figures out what the current host platform is and
    imports the adequate factory. The factory is the interface to all platform
    specific implementations.

    Args:
        factory (:obj:`module`): (optional) Provide a custom factory that is automatically returned unchanged.

    Returns: The suitable factory for the current host platform
        or the factory that was given as a argument.

    Raises:
        RuntimeError: If no supported host platform can be identified.
    """
    if factory is not None:
        return factory

    if current_platform == 'android':
        from toga_android import factory
        return factory
    elif current_platform == 'darwin':
        from toga_cocoa import factory
        return factory
    elif current_platform == 'ios':
        from toga_iOS import factory
        return factory
    elif current_platform == 'linux':
        from toga_gtk import factory
        return factory
    elif current_platform == 'tvos':
        from toga_tvOS import factory
        return factory
    elif current_platform == 'watchos':
        from toga_watchOS import factory
        return factory
    elif current_platform == 'web':
        from toga_web import factory
        return factory
    elif current_platform == 'win32':
        from toga_winforms import factory
        return factory
    else:
        raise RuntimeError(f"Unsupported host platform {current_platform!r}.")
