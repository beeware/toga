import pytest

import toga


@pytest.fixture
def parent_group_1():
    return toga.Group("P", order=1)


@pytest.fixture
def child_group_1(parent_group_1):
    return toga.Group("C", order=2, parent=parent_group_1)


@pytest.fixture
def child_group_2(parent_group_1):
    return toga.Group("B", order=4, parent=parent_group_1)


@pytest.fixture
def parent_group_2():
    return toga.Group("O", order=2)


@pytest.fixture
def child_group_3(parent_group_2):
    return toga.Group("A", order=2, parent=parent_group_2)
