import importlib
import sys
from functools import lru_cache

try:
    # Usually, the pattern is "import module; if it doesn't exist,
    # import the shim". However, we need the 3.10 API for entry_points,
    # as the 3.8 didn't support the `groups` argument to entry_points.
    # Therefore, we try to import the compatibility shim first; and fall
    # back to the stdlib module if the shim isn't there.
    from importlib_metadata import entry_points
except ImportError:
    from importlib.metadata import entry_points


# Map python sys.platform with toga platforms names
_TOGA_PLATFORMS = {
    'android': 'android',
    'darwin': 'macOS',
    'ios': 'iOS',
    'linux': 'linux',
    'tvos': 'tvOS',
    'watchos': 'watchOS',
    'wearos': 'wearOS',
    'web': 'web',
    'win32': 'windows',
}


# Rely on `sys.getandroidapilevel`, which only exists on Android; see
# https://github.com/beeware/Python-Android-support/issues/8
if hasattr(sys, 'getandroidapilevel'):
    current_platform = _TOGA_PLATFORMS.get('android')
else:
    current_platform = _TOGA_PLATFORMS.get(sys.platform)


def _entry_point_format(backend):
    return '{} ({})'.format(backend.name, backend.value)


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

    toga_backends = entry_points(group='toga.backends')
    if not toga_backends:
        raise RuntimeError("No toga backend could be loaded.")

    if len(toga_backends) == 1:
        my_backend = toga_backends[0]
    else:
        # multiple backends are installed: choose the one that maches the host platform
        backend_name = current_platform
        toga_backends_string = ', '.join([_entry_point_format(backend) for backend in toga_backends])
        my_backends = tuple(filter(lambda backend: backend.name == backend_name, toga_backends))
        if len(my_backends) != 1:
            raise RuntimeError(
                'Several toga backends installed: {}. '
                'Could not identify which one is more appropriate for your platform ({}).'
                .format(toga_backends_string, current_platform)
            )
        my_backend = my_backends[0]
        print(
            'WARNING: Several toga backends installed: {}. Using {}'.format(
                toga_backends_string, _entry_point_format(my_backend)
            )
        )

    factory = importlib.import_module('{}.factory'.format(my_backend.value))
    return factory
