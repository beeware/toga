import System.Windows.Forms as WinForms
from pytest import fixture
from tests.utils import set_get

import toga

TEXTS = ["", "a", "ab", "abc", "hello world"]


# TODO: refactor duplication with other widgets
@fixture
def widget(main_box):
    label = toga.Label("")
    main_box.add(label)
    yield label
    main_box.remove(label)


def test_native(widget, native, main_box):
    native_box = main_box._impl.native
    assert native_box.Controls.Count == 1
    # TODO: assert native_box.Controls[0] is native
    assert isinstance(native_box.Controls[0], WinForms.Label)


def test_text(widget, native):
    for text in TEXTS:
        set_get(widget, "text", text)
        assert native.Text == text
