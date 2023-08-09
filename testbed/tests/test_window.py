import gc
import weakref

import toga

# Mobile platforms have different windowing characteristics, so they have different tests.
if toga.platform.current_platform in {"iOS", "android"}:
    ####################################################################################
    # Mobile platform tests
    ####################################################################################

    pass
else:

    async def test_secondary_window_cleanup(app_probe):
        """Memory for windows is cleaned up when windows are deleted."""
        # Create and show a window with content. We can't use the second_window fixture
        # because the fixture will retain a reference, preventing garbage collection.
        second_window = toga.Window()
        toga.App.app.windows.add(second_window)
        second_window.content = toga.Box()
        second_window.show()
        await app_probe.redraw("Secondary Window has been created")

        # Retain a weak reference to the window to check garbage collection
        window_ref = weakref.ref(second_window)
        impl_ref = weakref.ref(second_window._impl)

        second_window.close()
        await app_probe.redraw("Secondary window has been closed")

        # Clear the local reference to the window (which should be the last reference),
        # and force a garbage collection pass. This should cause deletion of both the
        # interface and impl of the window.
        second_window = None
        gc.collect()

        # Assert that the weak references are now dead.
        assert window_ref() is None
        assert impl_ref() is None
