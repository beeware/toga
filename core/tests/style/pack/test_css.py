import pytest

from toga.colors import REBECCAPURPLE
from toga.style.pack import (
    BOLD,
    CENTER,
    COLUMN,
    END,
    HIDDEN,
    ITALIC,
    JUSTIFY,
    LEFT,
    LTR,
    NONE,
    NORMAL,
    PACK,
    RIGHT,
    ROW,
    RTL,
    SERIF,
    SMALL_CAPS,
    START,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    VISIBLE,
    Pack,
)


@pytest.mark.parametrize(
    "style, expected_css",
    [
        # Empty definition
        pytest.param(
            Pack(),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="empty",
        ),
        # Display
        pytest.param(
            Pack(display=PACK),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="display-pack",
        ),
        pytest.param(
            Pack(display=NONE),
            "display: none; flex-direction: row; flex: 0.0 0 auto;",
            id="display-none",
        ),
        # Visibility
        pytest.param(
            Pack(visibility=VISIBLE),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="visibility-visible",
        ),
        pytest.param(
            Pack(visibility=HIDDEN),
            "visibility: hidden; flex-direction: row; flex: 0.0 0 auto;",
            id="visibility-hidden",
        ),
        # Direction
        pytest.param(
            Pack(direction=ROW),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="direction-row",
        ),
        pytest.param(
            Pack(direction=COLUMN),
            "flex-direction: column; flex: 0.0 0 auto;",
            id="direction-column",
        ),
        # Width
        pytest.param(
            Pack(width=42),
            "flex-direction: row; width: 42px;",
            id="width-explicit",
        ),
        pytest.param(
            Pack(width=42, flex=5),
            "flex-direction: row; width: 42px;",
            id="width-explicit-flex",
        ),
        pytest.param(
            Pack(width=0),
            "flex-direction: row; width: 0px;",
            id="width-0",
        ),
        pytest.param(
            Pack(width=NONE),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="width-none",
        ),
        pytest.param(
            Pack(width=NONE, flex=5),
            "flex-direction: row; flex: 5.0 0 auto;",
            id="width-none-flex",
        ),
        pytest.param(
            Pack(direction=ROW, width=42),
            "flex-direction: row; width: 42px;",
            id="width-row-explicit",
        ),
        pytest.param(
            Pack(direction=ROW, width=42, flex=5),
            "flex-direction: row; width: 42px;",
            id="width-row-explicit-flex",
        ),
        pytest.param(
            Pack(direction=ROW, width=0),
            "flex-direction: row; width: 0px;",
            id="width-row-0",
        ),
        pytest.param(
            Pack(direction=ROW, width=NONE),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="width-row-none",
        ),
        pytest.param(
            Pack(direction=ROW, width=NONE, flex=5),
            "flex-direction: row; flex: 5.0 0 auto;",
            id="width-row-none-flex",
        ),
        pytest.param(
            Pack(direction=COLUMN, width=42),
            "flex-direction: column; flex: 0.0 0 auto; width: 42px;",
            id="width-column-explicit",
        ),
        pytest.param(
            Pack(direction=COLUMN, width=42, flex=5),
            "flex-direction: column; flex: 5.0 0 auto; width: 42px;",
            id="width-column-explicit-flex",
        ),
        pytest.param(
            Pack(direction=COLUMN, width=0),
            "flex-direction: column; flex: 0.0 0 auto; width: 0px;",
            id="width-column-0",
        ),
        pytest.param(
            Pack(direction=COLUMN, width=NONE),
            "flex-direction: column; flex: 0.0 0 auto;",
            id="width-column-none",
        ),
        pytest.param(
            Pack(direction=COLUMN, width=NONE, flex=5),
            "flex-direction: column; flex: 5.0 0 auto;",
            id="width-column-none-flex",
        ),
        # Height
        pytest.param(
            Pack(height=42),
            "flex-direction: row; flex: 0.0 0 auto; height: 42px;",
            id="height-explicit",
        ),
        pytest.param(
            Pack(height=42, flex=5),
            "flex-direction: row; flex: 5.0 0 auto; height: 42px;",
            id="height-explicit-flex",
        ),
        pytest.param(
            Pack(height=0),
            "flex-direction: row; flex: 0.0 0 auto; height: 0px;",
            id="height-0",
        ),
        pytest.param(
            Pack(height=NONE),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="height-none",
        ),
        pytest.param(
            Pack(height=NONE, flex=5),
            "flex-direction: row; flex: 5.0 0 auto;",
            id="height-none-flex",
        ),
        pytest.param(
            Pack(direction=ROW, height=42),
            "flex-direction: row; flex: 0.0 0 auto; height: 42px;",
            id="height-row-explicit",
        ),
        pytest.param(
            Pack(direction=ROW, height=42, flex=5),
            "flex-direction: row; flex: 5.0 0 auto; height: 42px;",
            id="height-row-explicit",
        ),
        pytest.param(
            Pack(direction=ROW, height=0),
            "flex-direction: row; flex: 0.0 0 auto; height: 0px;",
            id="height-row-0",
        ),
        pytest.param(
            Pack(direction=ROW, height=NONE),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="height-row-none",
        ),
        pytest.param(
            Pack(direction=ROW, height=NONE, flex=5),
            "flex-direction: row; flex: 5.0 0 auto;",
            id="height-row-none",
        ),
        pytest.param(
            Pack(direction=COLUMN, height=42),
            "flex-direction: column; height: 42px;",
            id="height-column-explicit",
        ),
        pytest.param(
            Pack(direction=COLUMN, height=42, flex=5),
            "flex-direction: column; height: 42px;",
            id="height-column-explicit-flex",
        ),
        pytest.param(
            Pack(direction=COLUMN, height=0),
            "flex-direction: column; height: 0px;",
            id="height-column-0",
        ),
        pytest.param(
            Pack(direction=COLUMN, height=NONE),
            "flex-direction: column; flex: 0.0 0 auto;",
            id="height-column-none",
        ),
        pytest.param(
            Pack(direction=COLUMN, height=NONE, flex=5),
            "flex-direction: column; flex: 5.0 0 auto;",
            id="height-column-none",
        ),
        # Alignment - default layout
        pytest.param(
            Pack(align_items=START),
            "flex-direction: row; flex: 0.0 0 auto; align-items: start;",
            id="align-items-start",
        ),
        pytest.param(
            Pack(align_items=END),
            "flex-direction: row; flex: 0.0 0 auto; align-items: end;",
            id="align-items-end",
        ),
        pytest.param(
            Pack(align_items=CENTER),
            "flex-direction: row; flex: 0.0 0 auto; align-items: center;",
            id="align-items-center",
        ),
        # Alignment - row layout
        pytest.param(
            Pack(direction=ROW, align_items=START),
            "flex-direction: row; flex: 0.0 0 auto; align-items: start;",
            id="row-align_items-start",
        ),
        pytest.param(
            Pack(direction=ROW, align_items=END),
            "flex-direction: row; flex: 0.0 0 auto; align-items: end;",
            id="row-align_items-end",
        ),
        pytest.param(
            Pack(direction=ROW, align_items=CENTER),
            "flex-direction: row; flex: 0.0 0 auto; align-items: center;",
            id="row-align_items-center",
        ),
        # Alignment - column layout
        pytest.param(
            Pack(direction=COLUMN, align_items=START),
            "flex-direction: column; flex: 0.0 0 auto; align-items: start;",
            id="column-align_items-start",
        ),
        pytest.param(
            Pack(direction=COLUMN, align_items=END),
            "flex-direction: column; flex: 0.0 0 auto; align-items: end;",
            id="column-align_items-end",
        ),
        pytest.param(
            Pack(direction=COLUMN, align_items=CENTER),
            "flex-direction: column; flex: 0.0 0 auto; align-items: center;",
            id="column-align_items-center",
        ),
        # justify_content
        pytest.param(
            Pack(justify_content=START),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="gap-start",
        ),
        pytest.param(
            Pack(justify_content=CENTER),
            "flex-direction: row; flex: 0.0 0 auto; justify-content: center;",
            id="gap-center",
        ),
        pytest.param(
            Pack(justify_content=END),
            "flex-direction: row; flex: 0.0 0 auto; justify-content: end;",
            id="gap-end",
        ),
        # Gap
        pytest.param(
            Pack(gap=42),
            "flex-direction: row; flex: 0.0 0 auto; gap: 42px;",
            id="gap",
        ),
        pytest.param(
            Pack(gap=0),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="gap-0",
        ),
        # Margin
        pytest.param(
            Pack(margin_top=42),
            "flex-direction: row; flex: 0.0 0 auto; margin-top: 42px;",
            id="margin-top",
        ),
        pytest.param(
            Pack(margin_bottom=42),
            "flex-direction: row; flex: 0.0 0 auto; margin-bottom: 42px;",
            id="margin-bottom",
        ),
        pytest.param(
            Pack(margin_left=42),
            "flex-direction: row; flex: 0.0 0 auto; margin-left: 42px;",
            id="margin-left",
        ),
        pytest.param(
            Pack(margin_right=42),
            "flex-direction: row; flex: 0.0 0 auto; margin-right: 42px;",
            id="margin-right",
        ),
        pytest.param(
            Pack(margin=42),
            (
                "flex-direction: row; flex: 0.0 0 auto; "
                "margin-top: 42px; margin-bottom: 42px; "
                "margin-left: 42px; margin-right: 42px;"
            ),
            id="margin",
        ),
        # Explicitly 0 margin
        pytest.param(
            Pack(margin_top=0),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="margin-top-0",
        ),
        pytest.param(
            Pack(margin_bottom=0),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="margin-bottom-0",
        ),
        pytest.param(
            Pack(margin_left=0),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="margin-left-0",
        ),
        pytest.param(
            Pack(margin_right=0),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="margin-right-0",
        ),
        pytest.param(
            Pack(margin=0),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="margin-0",
        ),
        # Color
        pytest.param(
            Pack(color=REBECCAPURPLE),
            "flex-direction: row; flex: 0.0 0 auto; color: rgb(102 51 153 / 1.0);",
            id="color",
        ),
        # Background Color
        pytest.param(
            Pack(background_color=REBECCAPURPLE),
            (
                "flex-direction: row; flex: 0.0 0 auto; "
                "background-color: rgb(102 51 153 / 1.0);"
            ),
            id="background-color",
        ),
        # Text Alignment
        pytest.param(
            Pack(text_align=LEFT),
            "flex-direction: row; flex: 0.0 0 auto; text-align: left;",
            id="text-align-left",
        ),
        pytest.param(
            Pack(text_align=RIGHT),
            "flex-direction: row; flex: 0.0 0 auto; text-align: right;",
            id="text-align-right",
        ),
        pytest.param(
            Pack(text_align=CENTER),
            "flex-direction: row; flex: 0.0 0 auto; text-align: center;",
            id="text-align-center",
        ),
        pytest.param(
            Pack(text_align=JUSTIFY),
            "flex-direction: row; flex: 0.0 0 auto; text-align: justify;",
            id="text-align-justify",
        ),
        # Text Direction
        pytest.param(
            Pack(text_direction=RTL),
            "flex-direction: row; flex: 0.0 0 auto; text-direction: rtl;",
            id="text-align-rtl",
        ),
        pytest.param(
            Pack(text_direction=LTR),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="text-align-ltr",
        ),
        # Font
        pytest.param(
            Pack(font_family="Helvetica"),
            "flex-direction: row; flex: 0.0 0 auto; font-family: Helvetica;",
            id="font-family",
        ),
        pytest.param(
            Pack(font_family="Times New Roman"),
            'flex-direction: row; flex: 0.0 0 auto; font-family: "Times New Roman";',
            id="font-family",
        ),
        pytest.param(
            Pack(font_family=["Times New Roman"]),
            'flex-direction: row; flex: 0.0 0 auto; font-family: "Times New Roman";',
            id="font-family",
        ),
        pytest.param(
            Pack(font_family=["Times New Roman", SERIF]),
            'flex-direction: row; flex: 0.0 0 auto; font-family: "Times New Roman", '
            "serif;",
            id="font-family",
        ),
        pytest.param(
            Pack(font_family=["Times New Roman", "Courier", SERIF]),
            'flex-direction: row; flex: 0.0 0 auto; font-family: "Times New Roman", '
            "Courier, serif;",
            id="font-family",
        ),
        pytest.param(
            Pack(font_family=SYSTEM),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="font-family-explicit-default",
        ),
        pytest.param(
            Pack(font_style=ITALIC),
            "flex-direction: row; flex: 0.0 0 auto; font-style: italic;",
            id="font-style",
        ),
        pytest.param(
            Pack(font_style=NORMAL),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="font-style-explicit-default",
        ),
        pytest.param(
            Pack(font_weight=BOLD),
            "flex-direction: row; flex: 0.0 0 auto; font-weight: bold;",
            id="font-weight",
        ),
        pytest.param(
            Pack(font_weight=NORMAL),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="font-weight-explicit-default",
        ),
        pytest.param(
            Pack(font_variant=SMALL_CAPS),
            "flex-direction: row; flex: 0.0 0 auto; font-variant: small-caps;",
            id="font-variant",
        ),
        pytest.param(
            Pack(font_variant=NORMAL),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="font-variant-explicit-default",
        ),
        pytest.param(
            Pack(font_size=42),
            "flex-direction: row; flex: 0.0 0 auto; font-size: 42pt;",
            id="font-size",
        ),
        pytest.param(
            Pack(font_size=SYSTEM_DEFAULT_FONT_SIZE),
            "flex-direction: row; flex: 0.0 0 auto;",
            id="font-size-explicit-default",
        ),
        pytest.param(
            Pack(
                font_family="Helvetica",
                font_style=ITALIC,
                font_weight=BOLD,
                font_variant=SMALL_CAPS,
                font_size=42,
            ),
            (
                "flex-direction: row; flex: 0.0 0 auto; "
                "font-family: Helvetica; "
                "font-size: 42pt; "
                "font-weight: bold; "
                "font-style: italic; "
                "font-variant: small-caps;"
            ),
            id="font-full",
        ),
    ],
)
def test_rendering(style, expected_css):
    """An empty style node can be rendered."""
    assert style.__css__() == expected_css
