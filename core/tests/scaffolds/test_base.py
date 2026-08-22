import toga
from toga_dummy.utils import (
    assert_action_performed,
    assert_action_performed_with,
)


def test_init_without_content(window, app):
    """A scaffold can be initialized without content and be used for a window."""
    scaffold = toga.Scaffold()
    window.content = scaffold

    assert_action_performed_with(window, "set scaffold", scaffold=scaffold._impl)
    assert_action_performed_with(scaffold, "set content", widget=None)
    assert_action_performed(scaffold, "refresh")
    assert window.content == scaffold
    assert window.scaffold == scaffold
    assert scaffold.app == app
    assert scaffold.window == window
    assert scaffold.content is None

    # Add content and it'll work.
    content2 = toga.Box()
    scaffold.content = content2
    assert content2.scaffold == scaffold
    assert_action_performed(scaffold, "refresh")
    assert_action_performed(content2, "refresh")
    assert window.content == scaffold
    assert scaffold.content == content2
    assert content2.window == window
    assert content2.app == app


def test_init_with_content(window, app):
    """A scaffold can be initialized with content and be used for a window."""
    content1 = toga.Box()
    scaffold = toga.Scaffold(content1)
    window.content = scaffold

    assert_action_performed_with(window, "set scaffold", scaffold=scaffold._impl)
    assert_action_performed_with(scaffold, "set content", widget=content1._impl)
    assert_action_performed(scaffold, "refresh")
    assert_action_performed(content1, "refresh")
    assert window.content == scaffold
    assert window.scaffold == scaffold
    assert scaffold.app == app
    assert scaffold.window == window
    assert scaffold.content == content1
    assert content1.window == window
    assert content1.app == app
    assert content1.scaffold == scaffold

    # Change content
    content2 = toga.Box()
    scaffold.content = content2
    assert content1.scaffold is None
    assert content2.scaffold == scaffold
    assert_action_performed(scaffold, "refresh")
    assert_action_performed(content2, "refresh")
    assert window.content == scaffold
    assert scaffold.content == content2
    assert content1.window is None
    assert content1.app is None
    assert content2.window == window
    assert content2.app == app

    # Detach content
    scaffold.content = None
    assert content1.scaffold is None
    assert content2.scaffold is None
    assert_action_performed(scaffold, "refresh")
    assert window.content == scaffold
    assert scaffold.content is None
    assert content1.window is None
    assert content1.app is None
    assert content2.window is None
    assert content2.app is None

    # Attach content, detach scaffold; scaffold should preserve
    # content
    scaffold.content = content1
    assert content1.scaffold is scaffold
    window.content = None
    assert window.content is None
    assert scaffold.content == content1
    assert content1.scaffold is scaffold
    assert scaffold.window is None
    assert scaffold.app is None
    assert content1.window is None
    assert content1.app is None


def test_content_movement(window, app):
    """Content may be moved from one scaffold to another scaffold."""
    scaffold1 = toga.Scaffold()
    scaffold2 = toga.Scaffold()

    window.content = scaffold1

    content1 = toga.Box()
    content2 = toga.Box()

    scaffold1.content = content1
    scaffold2.content = content2

    assert content1.scaffold == scaffold1
    assert content2.scaffold == scaffold2

    # Move scaffold2's content to scaffold1
    scaffold1.content = scaffold2.content

    assert scaffold1.content == content2
    assert scaffold2.content is None

    assert content1.scaffold is None
    assert content2.scaffold == scaffold1

    assert content1.window is None
    assert content1.app is None
    assert content2.window == window
    assert content2.app == app


def test_content_implicit_orphan(window, app):
    """Implicitly moving a child out of scaffold content does not affect root
    content."""
    scaffold1 = toga.Scaffold()
    scaffold2 = toga.Scaffold()

    window.content = scaffold1

    content1 = toga.Box()
    child = toga.Box()
    content1.add(child)

    scaffold1.content = content1

    assert content1.scaffold == scaffold1
    assert child.scaffold == scaffold1

    scaffold2.content = child

    assert scaffold1.content == content1
    assert scaffold2.content == child

    assert content1.scaffold == scaffold1
    assert child.scaffold == scaffold2

    assert child not in content1.children
    assert content1.window == window
    assert content1.app == app
