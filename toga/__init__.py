from __future__ import print_function, unicode_literals, absolute_import, division

# Examples of valid version strings
# NUM_VERSION = (0, 1, 3, 'dev')
# NUM_VERSION = (0, 1, 3, ('a', 1))
# NUM_VERSION = (0, 1, 3, ('a', 2))
# NUM_VERSION = (0, 1, 3, ('a', 2), 'dev')
# NUM_VERSION = (0, 1, 3, ('b', 1))
# NUM_VERSION = (0, 1, 3, ('b', 1), 'dev')
# NUM_VERSION = (0, 1, 3)

NUM_VERSION = (0, 0, 0)


def get_git_changeset():
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    import datetime
    import os
    import subprocess

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=repo_dir, universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


def part_string(part, i):
    """Convert a version number part into a string for concatentation.

    Makes the following transformations:
        * Any number into a string:
            1 -> '1'
        * Any tuple into flat concatenated string:
            ('a', 2) -> 'a2'
        * The string 'dev' in to a dvelopment version number:
            dev'-> dev20130412121314

    Also takes into account whether a prepended dot is required,
    based on the position of the part in the overall string.
    """
    if part == 'dev':
        timestamp = get_git_changeset()
        if timestamp:
            s = 'dev%s' % timestamp
        else:
            s = 'dev'
        if i > 0:
            s = '.' + s
    elif isinstance(part, tuple):
        s = ''.join(str(p) for p in part)
    else:
        s = str(part)
        if i > 0:
            s = '.' + s
    return s

VERSION = "".join(part_string(nv, i) for i, nv in enumerate(NUM_VERSION))

import sys, os

if sys.platform == 'darwin':
    if os.environ.get('TARGET_IPHONE_SIMULATOR') or os.environ.get('TARGET_IPHONE'):
        from .platform.ios.app import *
        from .platform.ios.widgets import *
    else:
        from .platform.cocoa.app import *
        from .platform.cocoa.window import *
        from .platform.cocoa.widgets import *

elif sys.platform == 'linux2':
    from .platform.gtk.app import *
    from .platform.gtk.window import *
    from .platform.gtk.widgets import *

elif sys.platform == 'win32':
    from .platform.win32.app import *
    from .platform.win32.window import *
    from .platform.win32.widgets import *

else:
    raise NotImplemented('Platform is not currently supported')
