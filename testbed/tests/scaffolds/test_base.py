from tests_backend.scaffolds.base import ScaffoldProbe

import toga


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
    scaffold_probe = ScaffoldProbe(scaffold)
    main_window.content = scaffold
    await main_window_probe.redraw("New scaffold has been set")

    # Should not impact other properties
    assert main_window.title == "Scaffold testing!"

    # Scaffold layout is correct
    await scaffold_probe.wait_for_layout()

    # Now add a toolbar.  If the backend does not implement toolbar then
    # the rest of the test would be SKIP but failures would occur before here.
    main_window.toolbar.add(app.cmd1, app.cmd2)
    await main_window_probe.redraw("Main window has a toolbar")
    assert main_window_probe.has_toolbar()

    scaffold = toga.Scaffold(content=toga.Box())
    scaffold_probe = ScaffoldProbe(scaffold)
    main_window.content = scaffold
    await main_window_probe.redraw("New scaffold has been set")

    # Should be preserved.
    # Still has toolbar
    assert main_window_probe.has_toolbar()
