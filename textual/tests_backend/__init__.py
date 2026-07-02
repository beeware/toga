from pytest import mark

UNIMPLEMENTED_TEST_MODULES = {
    "tests/app/test_dialogs.py",
    "tests/app/test_document_app.py",
    "tests/test_fonts.py",
    "tests/test_icons.py",
    "tests/test_images.py",
    "tests/test_statusicons.py",
    "tests/window/test_dialogs.py",
    "tests/window/test_window.py",
    "tests/widgets/canvas/test_canvas.py",
    "tests/widgets/canvas/test_deprecated_code.py",
    "tests/widgets/test_activityindicator.py",
    "tests/widgets/test_dateinput.py",
    "tests/widgets/test_detailedlist.py",
    "tests/widgets/test_divider.py",
    "tests/widgets/test_imageview.py",
    "tests/widgets/test_mapview.py",
    "tests/widgets/test_multilinetextinput.py",
    "tests/widgets/test_numberinput.py",
    "tests/widgets/test_optioncontainer.py",
    "tests/widgets/test_scrollcontainer.py",
    "tests/widgets/test_selection.py",
    "tests/widgets/test_slider.py",
    "tests/widgets/test_splitcontainer.py",
    "tests/widgets/test_table.py",
    "tests/widgets/test_timeinput.py",
    "tests/widgets/test_tree.py",
    "tests/widgets/test_webview.py",
}


def pytest_collection_modifyitems(items):
    skip_unimplemented = mark.skip(reason="This feature is not implemented on Textual.")
    for item in items:
        path = item.path.as_posix()
        if any(path.endswith(module) for module in UNIMPLEMENTED_TEST_MODULES):
            item.add_marker(skip_unimplemented)
