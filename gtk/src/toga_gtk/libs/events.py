##########################################################################
# This code is derived from asyncio-glib:
#
#     https://github.com/jhenstridge/asyncio-glib
#
# It includes patches from pull requests against that project:
#
#   * #9, contributed by Benjamin Berg
#   * #6, contributed by Niels Avonds
#
# ------------------------------------------------------------------------
# Copyright (C) James Henstridge
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this library; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
##########################################################################

import asyncio
import selectors

from .gtk import GLib


class _SelectorSource(GLib.Source):
    """A GLib source that gathers selectors."""

    def __init__(self):
        super().__init__()
        self._fd_to_tag = {}
        self._fd_to_events = {}
        self._iteration_timeout = 0

    def prepare(self):
        return False, self._iteration_timeout

    def check(self):
        return False

    def dispatch(self, callback, args):
        for fd, tag in self._fd_to_tag.items():
            condition = self.query_unix_fd(tag)
            events = self._fd_to_events.setdefault(fd, 0)
            if condition & GLib.IOCondition.IN:
                events |= selectors.EVENT_READ
            if condition & GLib.IOCondition.HUP:
                events |= selectors.EVENT_READ
            if condition & GLib.IOCondition.OUT:
                events |= selectors.EVENT_WRITE
            self._fd_to_events[fd] = events
        return GLib.SOURCE_CONTINUE

    def register(self, fd, events):
        assert fd not in self._fd_to_tag

        condition = GLib.IOCondition(0)
        if events & selectors.EVENT_READ:
            condition |= GLib.IOCondition.IN
            condition |= GLib.IOCondition.HUP
        if events & selectors.EVENT_WRITE:
            condition |= GLib.IOCondition.OUT
        self._fd_to_tag[fd] = self.add_unix_fd(fd, condition)

    def unregister(self, fd):
        tag = self._fd_to_tag.pop(fd)
        self.remove_unix_fd(tag)

    def get_events(self, fd):
        return self._fd_to_events.get(fd, 0)

    def clear(self):
        self._fd_to_events.clear()


class GLibSelector(selectors._BaseSelectorImpl):

    def __init__(self, context):
        super().__init__()
        self._context = context
        self._source = _SelectorSource()
        self._source.attach(self._context)

    def close(self):
        self._source.destroy()
        super().close()

    def register(self, fileobj, events, data=None):
        key = super().register(fileobj, events, data)
        self._source.register(key.fd, events)
        return key

    def unregister(self, fileobj):
        key = super().unregister(fileobj)
        self._source.unregister(key.fd)
        return key

    def select(self, timeout=None):
        # Calling .set_ready_time() always causes a mainloop iteration to finish.
        if timeout is not None:
            # Negative timeout implies immediate dispatch
            self._source._iteration_timeout = int(max(0, timeout) * 1000)
        else:
            self._source._iteration_timeout = -1

        self._source.clear()
        self._context.iteration(False)

        ready = []
        for key in self.get_map().values():
            events = self._source.get_events(key.fd) & key.events
            if events != 0:
                ready.append((key, events))
        return ready


class GtkEventLoop(asyncio.SelectorEventLoop):
    def __init__(self):
        selector = GLibSelector(GLib.MainContext.default())
        super().__init__(selector)
        self._clock_resolution = 1e-3


class GtkEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = GtkEventLoop
