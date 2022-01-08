from rubicon.objc import (  # noqa: F401
    SEL,
    CGFloat,
    CGRect,
    CGRectMake,
    NSArray,
    NSMakePoint,
    NSMakeRect,
    NSMutableArray,
    NSMutableDictionary,
    NSObject,
    NSPoint,
    NSRange,
    NSRect,
    NSSize,
    ObjCInstance,
    at,
    objc_method,
    send_super
)

from .appkit import *  # noqa: F401, F403
from .core_graphics import *  # noqa: F401, F403
from .core_text import *  # noqa: F401, F403
from .foundation import *  # noqa: F401, F403
from .webkit import *  # noqa: F401, F403


def NSPoint__repr__(self):
    return '<NSPoint x={} y={}>'.format(self.x, self.y)


def NSRect__repr__(self):
    return '<NSRect origin={} size={}>'.format(self.origin, self.size)


def NSSize__repr__(self):
    return '<NSSize width={} height={}>'.format(self.width, self.height)


NSPoint.__repr__ = NSPoint__repr__
NSRect.__repr__ = NSRect__repr__
NSSize.__repr__ = NSSize__repr__
