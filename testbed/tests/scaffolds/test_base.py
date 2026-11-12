import toga
from toga.colors import CORNFLOWERBLUE, REBECCAPURPLE
from toga.style import Pack

from ..widgets.probe import get_probe


async def test_no_content(main_window, main_window_probe):
    """An empty scaffold can be created and used for a window without errors."""
    scaffold = toga.Scaffold()
    main_window.content = scaffold
    await main_window_probe.redraw("Setting empty scaffold")
    # Should not error


async def test_no_change_in_title(app, main_window, main_window_probe):
    """A scaffold can be used as window content."""
    # main_window currently has an implicit scaffold; set title
    # to make sure to test that it propagates onto new scaffold
    main_window.title = "Scaffold testing!"
    await main_window_probe.redraw("Setting initial window title")

    scaffold = toga.Scaffold(content=toga.Box())
    main_window.content = scaffold
    await main_window_probe.redraw("New scaffold has been set")

    # Should not impact other properties
    assert main_window.title == "Scaffold testing!"

    # Window layout is correct
    await main_window_probe.wait_for_window("Waiting for window layout")

    # Now add a toolbar.  If the backend does not implement toolbar then
    # the rest of the test would be SKIP but failures would occur before here.
    main_window.toolbar.add(app.cmd1, app.cmd2)
    await main_window_probe.redraw("Main window has a toolbar")
    assert main_window_probe.has_toolbar()

    scaffold = toga.Scaffold(content=toga.Box())
    main_window.content = scaffold
    await main_window_probe.redraw("New scaffold has been set")

    # Should be preserved.
    # Still has toolbar
    assert main_window_probe.has_toolbar()


async def test_scaffold_reinstated(main_window, main_window_probe):
    """A scaffold that has been replaced can be reinstated, with its content intact."""
    box1 = toga.Box(style=Pack(background_color=REBECCAPURPLE))
    scaffold1 = toga.Scaffold(content=box1)
    main_window.content = scaffold1
    await main_window_probe.wait_for_window("First scaffold installed")
    assert main_window.scaffold is scaffold1
    assert box1.window is main_window

    box2 = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
    scaffold2 = toga.Scaffold(content=box2)
    main_window.content = scaffold2
    await main_window_probe.wait_for_window("Second scaffold installed")
    assert main_window.scaffold is scaffold2
    assert box1.window is None
    assert box2.window is main_window

    main_window.content = scaffold1
    await main_window_probe.wait_for_window("First scaffold reinstated")
    assert main_window.scaffold is scaffold1
    assert box1.window is main_window
    assert box2.window is None

    # The reinstated content has been laid out and is visible at a real size.
    box_probe = get_probe(box1)
    await box_probe.redraw("Reinstated content is visible")
    assert box1.layout.content_width > 0
    assert box1.layout.content_height > 0
    assert box_probe.width > 0
    assert box_probe.height > 0
