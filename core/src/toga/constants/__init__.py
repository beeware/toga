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
