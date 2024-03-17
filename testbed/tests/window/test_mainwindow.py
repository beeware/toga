import re
from importlib import import_module

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE
from toga.style.pack import COLUMN, Pack


def window_probe(app, window):
    module = import_module("tests_backend.window")
    return module.WindowProbe(app, window)


@pytest.fixture
async def second_window(second_window_kwargs):
    yield toga.MainWindow(**second_window_kwargs)


@pytest.fixture
def default_window_title():
    return "Toga Testbed"


@pytest.fixture
async def second_window_probe(app, app_probe, second_window):
    second_window.show()
    probe = window_probe(app, second_window)
    await probe.wait_for_window(f"Window ({second_window.title}) has been created")
    yield probe
    if second_window in app.windows:
        second_window.close()


async def test_title(main_window, main_window_probe):
    """The title of the main window can be changed"""
    original_title = main_window.title
    assert original_title == "Toga Testbed"
    await main_window_probe.wait_for_window("Main Window title can be retrieved")

    try:
        main_window.title = "A Different Title"
        assert main_window.title == "A Different Title"
        await main_window_probe.wait_for_window("Main Window title can be changed")
    finally:
        main_window.title = original_title
        assert main_window.title == "Toga Testbed"
        await main_window_probe.wait_for_window("Main Window title can be reverted")


# Mobile platforms have different windowing characterics, so they have different tests.
if toga.platform.current_platform in {"iOS", "android"}:
    ####################################################################################
    # Mobile platform tests
    ####################################################################################

    async def test_secondary_window():
        """A secondary main window cannot be created"""
        with pytest.raises(
            RuntimeError,
            match=r"Secondary windows cannot be created on mobile platforms",
        ):
            toga.MainWindow()

    async def test_move_and_resize(main_window, main_window_probe, capsys):
        """Move and resize are no-ops on mobile."""
        initial_size = main_window.size
        content_size = main_window_probe.content_size
        assert initial_size[0] > 300
        assert initial_size[1] > 500

        assert main_window.position == (0, 0)

        main_window.position = (150, 50)
        await main_window_probe.wait_for_window("Main window can't be moved")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        main_window.size = (200, 150)
        await main_window_probe.wait_for_window("Main window cannot be resized")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        try:
            orig_content = main_window.content

            box1 = toga.Box(
                style=Pack(background_color=REBECCAPURPLE, width=10, height=10)
            )
            box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=20))
            main_window.content = toga.Box(
                children=[box1, box2],
                style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
            )
            await main_window_probe.wait_for_window("Main window content has been set")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            # Alter the content width to exceed window width
            box1.style.width = 1000
            await main_window_probe.wait_for_window(
                "Content is too wide for the window"
            )
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            space_warning = (
                r"Warning: Window content \([\d.]+, [\d.]+\) "
                r"exceeds available space \([\d.]+, [\d.]+\)"
            )
            assert re.search(space_warning, capsys.readouterr().out)

            # Resize content to fit
            box1.style.width = 100
            await main_window_probe.wait_for_window("Content fits in window")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size
            assert not re.search(space_warning, capsys.readouterr().out)

            # Alter the content width to exceed window height
            box1.style.height = 2000
            await main_window_probe.wait_for_window(
                "Content is too tall for the window"
            )
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size
            assert re.search(space_warning, capsys.readouterr().out)

        finally:
            main_window.content = orig_content

    async def test_full_screen(main_window, main_window_probe):
        """Window can be made full screen"""
        main_window.full_screen = True
        await main_window_probe.wait_for_window("Full screen is a no-op")

        main_window.full_screen = False
        await main_window_probe.wait_for_window("Full screen is a no-op")

    async def test_screen(main_window, main_window_probe):
        """The window can be relocated to another screen, using both absolute and relative screen positions."""
        assert main_window.screen.origin == (0, 0)
        initial_size = main_window.size
        main_window.position = (150, 50)
        await main_window_probe.wait_for_window("Main window can't be moved")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)
        assert main_window.screen_position == (0, 0)

else:
    ####################################################################################
    # Desktop platform tests
    ####################################################################################

    from .test_window import (  # noqa: F401
        test_full_screen,
        test_move_and_resize,
        test_non_closable,
        test_non_minimizable,
        test_non_resizable,
        test_screen,
        test_secondary_window,
        test_secondary_window_cleanup,
        test_secondary_window_with_args,
        test_visibility,
    )

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Secondary Window", position=(200, 300), size=(400, 200))],
    )
    async def test_secondary_window_toolbar(app, second_window, second_window_probe):
        """A toolbar can be added to a secondary window"""
        second_window.toolbar.add(app.cmd1)

        # Window doesn't have content. This is intentional.
        second_window.show()

        assert second_window_probe.has_toolbar()
        await second_window_probe.redraw("Secondary window has a toolbar")


async def test_as_image(main_window, main_window_probe):
    """The window can be captured as a screenshot"""

    screenshot = main_window.as_image()
    main_window_probe.assert_image_size(
        screenshot.size,
        main_window_probe.content_size,
        screen=main_window.screen,
    )
