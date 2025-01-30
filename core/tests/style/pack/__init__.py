from toga.style.pack import Pack


def with_init(**kwargs):
    return Pack(**kwargs)


def with_update(**kwargs):
    style = Pack()
    style.update(**kwargs)
    return style


def with_setattr(**kwargs):
    style = Pack()
    for name, value in kwargs.items():
        setattr(style, name, value)
    return style


def with_setitem(**kwargs):
    style = Pack()
    for name, value in kwargs.items():
        style[name] = value
    return style


def with_setitem_hyphen(**kwargs):
    style = Pack()
    for name, value in kwargs.items():
        style[name.replace("_", "-")] = value
    return style


def getitem(obj, name):
    return obj[name]


def getitem_hyphen(obj, name):
    return obj[name.replace("_", "-")]


def delitem(obj, name):
    del obj[name]


def delitem_hyphen(obj, name):
    del obj[name.replace("_", "-")]
