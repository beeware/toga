from . import Gtk


def apply_gtk_style(style_context, style):
    # creating StyleProvider (i.e CssProvider)
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(style.encode())

    # setting the StyleProvider to StyleContext
    style_context.add_provider(
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )
    style_context.add_class("toga")


def get_color_css(value):
    return (
        ".toga {"
        f"color: rgba({value.r}, {value.g}, {value.b}, {value.a});"
        "}"
    )


def get_bg_color_css(value):
    return (
        ".toga {"
        f"background-color: rgba({value.r}, {value.g}, {value.b}, {value.a});"
        "background-image: none;"
        "}"
    )


def get_font_css(value):
    style = (
        ".toga { "
        f"font-style: {value.style}; "
        f"font-variant: {value.variant}; "
        f"font-weight: {value.weight}; "
        f"font-family: {value.family}; "
    )

    if value.size != -1:
        style += f"font-size: {value.size}px; "

    style += "}"
    return style
