class StyleProperty:
    def __set_name__(self, mixin_cls, name):
        self.name = name

    def __repr__(self):
        return f"<StyleProperty {self.name!r}>"

    def __get__(self, widget, mixin_cls):
        return self if widget is None else getattr(widget.style, self.name)

    def __set__(self, widget, value):
        setattr(widget.style, self.name, value)

    def __delete__(self, widget):
        delattr(widget.style, self.name)


def style_mixin(style_cls):
    mixin_dict = {
        "__doc__": f"""
            Allows accessing the {style_cls.__name__} {style_cls._doc_link} directly on
            the widget. For example, instead of ``widget.style.color``, you can simply
            write ``widget.color``.
            """
    }

    try:
        _all_properties = style_cls._BASE_ALL_PROPERTIES
    except AttributeError:
        # Travertino 0.3 compatibility
        _all_properties = style_cls._ALL_PROPERTIES

    for name in _all_properties[style_cls]:
        mixin_dict[name] = StyleProperty()

    return type(style_cls.__name__ + "Mixin", (), mixin_dict)
