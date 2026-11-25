import pytest

import toga

from ..conftest import skip_on_backends

####################################################################################
# Windows platform tests
####################################################################################
if toga.platform.current_platform != "windows":
    pytest.skip("Test is specific to Windows", allow_module_level=True)

skip_on_backends(
    "toga_textual",
    reason="WinForms lifecycle hooks are not available on Textual.",
    allow_module_level=True,
)


def test_application_lifecycle_hooks(app):
    """The Windows app exposes native application lifecycle hooks."""

    impl = app._impl

    assert callable(impl.winforms_application_exit)
    assert callable(impl.winforms_thread_exit)
    assert callable(impl.winforms_enter_thread_modal)
    assert callable(impl.winforms_leave_thread_modal)
    assert callable(impl.winforms_idle)
