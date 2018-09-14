import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402
from toga.constants import LEFT, RIGHT, CENTER, JUSTIFY  # noqa: E402

try:
    text = unicode
except NameError:
    text = str


def gtk_alignment(alignment):
    "Convert Toga alignments in to arguments compatible with Gtk.set_alignment"
    return {
        LEFT: (0.0, 0.5),
        RIGHT: (1.0, 0.5),
        CENTER: (0.5, 0.5),
        JUSTIFY: (0.0, 0.0),
    }[alignment]


def gtk_apply_css(widget, css_rule):
    """Set custom css styles for Gtk widgets

    Args:
        widget (Gtk.Widget): CSS rule is applied to this Gtk widget
        css_rule (dict): An attribute-value Gtk CSS property pair
    """

    # Create style and convert to binary data
    css = bytes(generate_css(widget.get_css_name(), css_rule), 'utf-8')

    # Load CSS
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)

    # Apply CSS to widget
    style_context = widget.get_style_context()
    Gtk.StyleContext.add_provider(style_context, style_provider,
                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def generate_css(selector, decls):
    """Generate Gtk CSS from property-value pairs for a single selector

    Args:
        selector (str): Properties are applied to this CSS selector
        decls (dict): An attribute-value Gtk CSS property pair

    Returns:
        A Gtk CSS rule as a ``str``

    Raises:
        ``ValueError`` on empty arguments
    """

    if selector == '' or decls == {}:
        raise ValueError('Cannot create CSS rule with empty arguments!')

    res = selector + ' {\n'
    for attr, val in decls.items():
        res += '\t{attr}: {val};\n'.format(attr=attr, val=val)
    res += '}'

    return res
