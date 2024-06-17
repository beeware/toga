from enum import Enum, auto

from travertino.constants import *  # noqa: F401, F403  pragma: no cover


class Direction(Enum):
    """The direction a given property should act."""

    HORIZONTAL = 0
    VERTICAL = 1


class Baseline(Enum):
    """The meaning of a Y coordinate when drawing text."""

    ALPHABETIC = auto()  #: Alphabetic baseline of the first line
    TOP = auto()  #: Top of text
    MIDDLE = auto()  #: Middle of text
    BOTTOM = auto()  #: Bottom of text


class FillRule(Enum):
    """The rule to use when filling paths."""

    EVENODD = 0
    NONZERO = 1


##########################################################################
# Camera
##########################################################################


class FlashMode(Enum):
    """The flash mode to use when capturing photos or videos."""

    # These constant values allow `flash=True` and `flash=False` to work
    AUTO = -1
    OFF = 0
    ON = 1

    def __str__(self) -> str:
        return self.name.title()


# class VideoQuality(Enum):
#     """The quality of the video recording.
#
#     The values of ``LOW``, ``MEDIUM`` and ``HIGH`` represent specific (platform
#     dependent) resolutions. These resolutions will remain the same over time.
#
#     The values of ``CELLULAR`` and ``WIFI`` may change over time to reflect the
#     capabilities of network hardware.
#
#     ``HIGHEST`` will always refer to the highest quality that the device can
#     record.
#     """
#
#     LOW = 0
#     MEDIUM = 1
#     HIGH = 2
#
#     # Qualitative alternatives to these constants
#     CELLULAR = 0
#     WIFI = 1
#     HIGHEST = 2

##########################################################################
# Window States
##########################################################################


class WindowState(Enum):
    """The possible window states of an app."""

    MAXIMIZED = auto()
    """``MAXIMIZED`` state is when the window title bar and window chrome,
    along with app menu and toolbars remain **visible**."""

    FULLSCREEN = auto()
    """``FULLSCREEN`` state is when the window title bar and window chrome
    remain **hidden**; But app menu and toolbars remain **visible**."""

    PRESENTATION = auto()
    """``PRESENTATION`` state is when the window title bar, window chrome,
    app menu and toolbars all remain **hidden**.

    A good example of "full screen" mode is a slideshow app in presentation
    mode - the only visible content is the slide."""

    MINIMIZED = auto()
    """``MINIMIZED`` state is:

    For Desktop Platforms:
        When the window is in the form of an icon or preview image and is placed in the:
            * Taskbar - For Windows
            * Dock - For macOS
            * Area analogous to Taskbar or Dock - For Linux - Depending upon the DE

    For Mobile Platforms:
        When the App is in the background

    """
    NORMAL = auto()
    """``NORMAL`` state is when the window/app is not in any of the above window states.

    On Mobile Platforms(Like on Android) - Once the app is in minimized/background state, then
    it is currently not possible to bring the app to foreground by setting window state to
    ``NORMAL``. This is because of the design decisions imposed by the native mobile platforms.
    (i.e., to prevent apps from becoming intrusively foreground against the user's wishes.)
    """
