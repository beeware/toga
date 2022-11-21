import System.Windows.Forms as WinForms
from pytest import fixture
from System import Object

import toga

from ..test_utils import set_get

TEXTS = ["", "a", "ab", "abc", "hello world"]


# TODO: refactor duplication with other widgets
@fixture
async def widget(main_box):
    label = toga.Label("")
    main_box.add(label)
    yield label
    main_box.remove(label)


async def test_native(widget, native, main_box):
    native_box = main_box._impl.native
    assert native_box.Controls.Count == 1
    assert Object.ReferenceEquals(native_box.Controls[0], native)
    assert isinstance(native, WinForms.Label)


async def test_text(widget, native):
    for text in TEXTS:
        set_get(widget, "text", text)
        assert native.Text == text
