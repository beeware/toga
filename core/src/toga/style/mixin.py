from travertino.declaration import directional_property, validated_property


class StyleProperty:
    def __set_name__(self, mixin_cls, name):
        self.name = name

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

    for name in dir(style_cls):
        if not name.startswith("_") and isinstance(
            getattr(style_cls, name), (validated_property, directional_property)
        ):
            mixin_dict[name] = StyleProperty()

    return type(style_cls.__name__ + "Mixin", (), mixin_dict)
