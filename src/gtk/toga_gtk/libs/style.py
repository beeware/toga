from . import Gtk


def apply_color(style_context, value):
    # creating css
    style = (
        ".custom-style {"
        f"color: rgba({value.r}, {value.g}, {value.b}, {value.a});"
        "}"
    )

    # creating StyleProvider (i.e CssProvider)
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(style.encode())

    # setting the StyleProvider to StyleContext
    style_context.add_provider(
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )
    style_context.add_class("custom-style")


def apply_bg_color(style_context, value):
    # creating css
    style = (
        ".custom-style {"
        f"background-color: rgba({value.r}, {value.g}, {value.b}, {value.a});"
        "background-image: none;"
        "}"
    )

    # creating StyleProvider (i.e CssProvider)
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(style.encode())

    # setting the StyleProvider to StyleContext
    style_context.add_provider(
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )
    style_context.add_class("custom-style")


def apply_font(style_context, value):
    # creating css
    style = (
        ".custom-style { "
        f"font-style: {value.style}; "
        f"font-variant: {value.variant}; "
        f"font-weight: {value.weight}; "
    )

    if value.family != "system":
        style += f"font-family: {value.family}; "
    if value.size != -1:
        style += f"font-size: {value.size}px; "

    style += "}"

    # creating StyleProvider (i.e CssProvider)
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(style.encode())

    # setting the StyleProvider to StyleContext
    style_context.add_provider(
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )
    style_context.add_class("custom-style")
