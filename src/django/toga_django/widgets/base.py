from toga.interface.widgets.base import Widget


class WidgetMixin:
    def handler(self, fn, name):
        if hasattr(fn, '__self__'):
            ref = '(%s,%s-%s)' % (fn.__self__.id, self.id, name)
        else:
            ref = '%s-%s' % (self.id, name)

        return ref

    @property
    def ports(self):
        return ",".join(
            "%s=%s" % (name, widget.id)
            for name, widget in self.__dict__.items()
            if isinstance(widget, Widget)
        )

    def _set_app(self, app):
        pass

    def _set_window(self, window):
        pass

    def _set_container(self, container):
        # if self._constraints and self._impl:
            # self._container._impl.addSubview_(self._impl)
            # self._constraints._container = container
        self.rehint()

    def _add_child(self, child):
        pass
        # if self._container:
            # child._set_container(self._container)

    def _add_constraints(self):
        pass
        # self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self._constraints = Constraints(self)

    def _apply_layout(self):
        pass
        # if self._constraints:
        #     self._constraints.update()

    def rehint(self):
        pass

    def _set_font(self, font):
        # self._impl.setFont_(font._impl)
        pass

    def _set_app(self, app):
        pass
    #     app.support_module.__dict__[self.IMPL_CLASS.__name__] = self.IMPL_CLASS

    # def _update_layout(self, **style):
    #     """Force a layout update on the widget.

    #     The update request can be accompanied by additional style information
    #     (probably min_width, min_height, width or height) to control the
    #     layout.
    #     """
    #     if self._in_progress:
    #         return
    #     self._in_progress = True

    #     self.style(**style)

    #     # Recompute layout
    #     layout = self.layout
    #     print("WIDGET LAYOUT", layout)

    #     # Set the frame for the widget to adhere to the new style.
    #     self._set_frame(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))

    #     self._update_child_layout(**style)

    #     # Set the frame for the widget to adhere to the new style.
    #     self._set_child_frames()

    #     self._in_progress = False

    # def _set_frame(self, frame):
    #     print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
    #     self._impl.setFrame_(frame)
    #     self._impl.setNeedsDisplay_(True)

    # def _update_child_layout(self, **style):
    #     """Force a layout update on children of this widget.

    #     By default, do nothing; widgets have no children
    #     """
    #     pass

    # def _set_child_frames(self):
    #     pass
