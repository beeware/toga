from __future__ import print_function, absolute_import, division

from colosseum import CSSNode

from rubicon.objc import NSSize, NSRect, NSPoint


class Widget(object):
    def __init__(self):
        self._window = None
        self._app = None
        self._impl = None
        self._css = CSSNode()

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Widget %r is already associated with an App" % self)
        self._app = app
        self._set_app(app)

    def _set_app(self, app):
        pass

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        self._set_window(window)

    def _set_window(self, window):
        pass

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, id(self))

    def style(self, **styles):
        for style, value in styles.items():
            if style in ('margin', 'borderWidth', 'padding'):
                if style == 'borderWidth':
                    pre = 'border'
                    post = 'Width'
                else:
                    pre = style
                    post = ''

                try:
                    if len(value) == 4:
                        setattr(self._css, pre + 'Top' + post, value)
                        setattr(self._css, pre + 'Right' + post, value)
                        setattr(self._css, pre + 'Bottom' + post, value)
                        setattr(self._css, pre + 'Left' + post, value)
                    elif len(value) == 3:
                        setattr(self._css, pre + 'Top' + post, value)
                        setattr(self._css, pre + 'Right' + post, value)
                        setattr(self._css, pre + 'Bottom' + post, value)
                        setattr(self._css, pre + 'Left' + post, value)
                    elif len(value) == 2:
                        setattr(self._css, pre + 'Top' + post, value)
                        setattr(self._css, pre + 'Right' + post, value)
                        setattr(self._css, pre + 'Bottom' + post, value)
                        setattr(self._css, pre + 'Left' + post, value)
                    elif len(value) == 1:
                        setattr(self._css, pre + 'Top' + post, value)
                        setattr(self._css, pre + 'Right' + post, value)
                        setattr(self._css, pre + 'Bottom' + post, value)
                        setattr(self._css, pre + 'Left' + post, value)
                    else:
                        raise Exception('Invalid %s definition' % style)
                except TypeError:
                    setattr(self._css, pre + 'Top' + post, value)
                    setattr(self._css, pre + 'Right' + post, value)
                    setattr(self._css, pre + 'Bottom' + post, value)
                    setattr(self._css, pre + 'Left' + post, value)
            else:
                setattr(self._css, style, value)

    def _update_layout(self):
        layout = self._css.layout
        self._impl.setFrame_(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))
