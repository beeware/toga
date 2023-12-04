import pytest

import toga


@pytest.fixture
def parent_group_1():
    return toga.Group("P1", order=1)


@pytest.fixture
def child_group_1(parent_group_1):
    return toga.Group("C1", order=2, parent=parent_group_1)


@pytest.fixture
def child_group_2(parent_group_1):
    return toga.Group("C2", order=4, parent=parent_group_1)


@pytest.fixture
def parent_group_2():
    return toga.Group("P2", order=2)


@pytest.fixture
def child_group_3(parent_group_2):
    return toga.Group("C3", section=2, order=2, parent=parent_group_2)


@pytest.fixture
def child_group_4(parent_group_2):
    return toga.Group("C4", section=2, order=1, parent=parent_group_2)


@pytest.fixture
def child_group_5(parent_group_2):
    return toga.Group("C5", section=1, order=1, parent=parent_group_2)
