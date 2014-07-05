import inspect

from .libs import *


class LongRunningTask_impl(object):
    LongRunningTask = ObjCSubclass('NSObject', 'LongRunningTask')

    @LongRunningTask.method('v@')
    def performIteration_(self, info):
        try:
            delay = self.interface.next()
            NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(delay, self, get_selector('performIteration:'), None, False)
        except StopIteration:
            pass

LongRunningTask = ObjCClass('LongRunningTask')


def process_callback(callback_result):
    "Handle generators in actions"
    if inspect.isgenerator(callback_result):
        task = LongRunningTask.alloc().init()
        task.interface = callback_result
        task.performIteration_(None)
