from unittest.mock import Mock

import pytest

import toga
from toga.sources import Source, TreeSource
from toga.sources.tree_source import Node
from toga_dummy.utils import assert_action_performed


@pytest.fixture
def headings():
    return [f"Heading {x}" for x in range(3)]


@pytest.fixture
def accessors():
    return [f"heading{i}" for i in range(3)]


@pytest.fixture
def missing_value():
    return "---"


@pytest.fixture
def dict_data():
    return {
        ("one", 1): [
            ("one.one", 1.1),
            ("one.two", 2.1),
        ],
        ("two", 2): None,
    }


@pytest.fixture
def treesource_data(dict_data, accessors):
    return TreeSource(dict_data, accessors)


@pytest.fixture
def list_data(dict_data):
    return list(dict_data.keys())


@pytest.fixture
def tuple_data(dict_data):
    return tuple(dict_data.keys())


@pytest.fixture
def mysource_headings():
    return ["Item name", "Item value"]


@pytest.fixture
def mysource_accessors():
    return ["name", "value"]


@pytest.fixture
def mysource_data():
    class MySource(Source):
        def __init__(self, data):
            super().__init__()
            self._data = data

        def __len__(self):
            return len(self._data)

        def __getitem__(self, index):
            return self._data[index]

        def can_have_children(self):
            return True

    class MyNode:
        def __init__(self, name, value, children=None):
            self._name = name
            self._value = value
            self._children = children

        @property
        def name(self):
            return self._name

        @property
        def value(self):
            return self._value

        def __len__(self):
            return len(self._children)

        def __getitem__(self, index):
            return self._children[index]

        def can_have_children(self):
            return self._children is not None

    return MySource(
        [
            MyNode(
                "one",
                1,
                children=[
                    MyNode("one.one", 1.1),
                    MyNode("one.two", 1.2),
                ],
            ),
            MyNode("two", 2, children=[]),
        ]
    )


@pytest.fixture
def tree(headings, missing_value):
    return toga.Tree(headings=headings, missing_value=missing_value)


def test_widget_created(tree, headings, missing_value):
    "A tree widget can be created"
    assert tree._impl.interface is tree
    assert_action_performed(tree, "create Tree")
    assert isinstance(tree.data, TreeSource)
    assert tree.headings is headings
    assert tree.missing_value is missing_value
    assert len(tree.data) == 0


def test_widget_not_created():
    "A tree widget cannot be created without arguments"
    with pytest.raises(ValueError):
        _ = toga.Tree()


@pytest.mark.parametrize(
    "value, expected",
    [
        (False, False),
        (True, True),
    ],
)
def test_multiselect(headings, value, expected):
    "The multiselect status of the widget can be set."
    # Widget is initially not multiselect.
    tree = toga.Tree(headings=headings, data=None)
    assert tree.multiple_select is False

    # Set multiselect explicitly.
    tree = toga.Tree(headings=headings, data=None, multiple_select=value)
    assert tree.multiple_select is expected

    # Cannot change multiselect
    with pytest.raises(AttributeError):
        tree.multiple_select = not value


def test_selection(tree):
    "The selection property can be read."
    _ = tree.selection
    assert_action_performed(tree, "get selection")


def test_on_select(tree):
    "The on_select handler can be invoked."
    # No handler initially
    assert tree._on_select._raw is None

    # Define and set a new callback
    handler = Mock()

    tree.on_select = handler

    assert tree.on_select._raw == handler

    # Invoke the callback
    tree._impl.simulate_select()

    # Callback was invoked
    handler.assert_called_once_with(tree)


def test_on_double_click(tree):
    "The on_double_click handler can be invoked."
    # No handler initially
    assert tree._on_double_click._raw is None

    # Define and set a new callback
    handler = Mock()

    tree.on_double_click = handler

    assert tree.on_double_click._raw == handler

    # Invoke the callback
    tree._impl.simulate_double_click()

    # Callback was invoked
    handler.assert_called_once_with(tree)


def test_accessor_synthesis_list_of_tuples():
    "Accessors are synthesized from a list of tuples, when no headings nor accessors are provided."
    data = [
        ("one", 1),
        ("two", 2),
    ]
    tree = toga.Tree(data=data)
    assert isinstance(tree.data, TreeSource)
    assert isinstance(tree.data[0], Node)

    # Accessors are syntesized
    assert len(tree._accessors) == 2
    with pytest.raises(AttributeError):
        _ = tree.data[0].heading0 == "one"
    assert tree.data[0].can_have_children() is False


def test_accessor_synthesis_dict_of_tuples():
    "Accessors are synthesized from a dict of tuples, when no headings nor accessors are provided."
    data = {
        ("one", 1): None,
        ("two", 2): None,
    }
    tree = toga.Tree(data=data)
    assert isinstance(tree.data, TreeSource)
    assert isinstance(tree.data[0], Node)

    # Accessors are syntesized
    assert len(tree._accessors) == 2
    with pytest.raises(AttributeError):
        _ = tree.data[0].heading0 == "one"
    assert tree.data[0].can_have_children() is False


def test_accessor_inference_list_of_dicts():
    "Accessors are infered from a list of dicts, if no headings nor accessors are provided."
    data = [
        {"heading0": "one", "heading1": 1},
        {"heading0": "two", "heading1": 2},
    ]
    tree = toga.Tree(data=data)
    assert isinstance(tree.data, TreeSource)
    assert isinstance(tree.data[0], Node)

    # Accessors are taken from the data
    assert len(tree._accessors) == 2
    assert tree.data[0].heading0 == "one"
    assert tree.data[0].can_have_children() is False


def test_invalid_data():
    "Accessors cannot be infered from data of wrong type."
    data = {
        ("one", 1),
        ("two", 2),
    }
    with pytest.raises(TypeError):
        _ = toga.Tree(data=data)


def test_invalid_values():
    "Accessors cannot be infered from data values of wrong type."
    data = [
        "one",
        "two",
    ]
    with pytest.raises(TypeError):
        _ = toga.Tree(data=data)


def test_mixed_native_data(headings, accessors):
    "Heterogeneous data can be be provided."
    data = {
        ("one", 1): [
            ("one.one", 1.1),
            ("one.two", (toga.Icon.DEFAULT_ICON, 1.2)),
            ((toga.Icon.DEFAULT_ICON, "one.three"), 1.3),
            {accessors[0]: "one.four", accessors[1]: 1.4},
            {accessors[1]: (toga.Icon.DEFAULT_ICON, 1.5), accessors[0]: "one.five"},
        ],
        ("two", 2): {
            ("two.one", 2.1): [
                ("two.one.one", "2.1.1"),
            ],
            ("two.two", 2.2): None,
        },
        ("three", 3): None,
        ("four", 4): {},
        ("five", 5): [],
    }
    tree = toga.Tree(headings=headings, data=data, accessors=accessors)
    assert isinstance(tree.data, TreeSource)
    assert isinstance(tree.data[0], Node)
    assert tree.data[0].heading0 == "one"
    assert tree.data[0][0].heading0 == "one.one"
    assert tree.data[0][0].heading1 == 1.1
    assert tree.data[0][1].heading1 == (toga.Icon.DEFAULT_ICON, 1.2)
    assert tree.data[0][2].heading0 == (toga.Icon.DEFAULT_ICON, "one.three")
    assert tree.data[0][3].heading1 == 1.4
    assert tree.data[0][4].heading1 == (toga.Icon.DEFAULT_ICON, 1.5)
    assert tree.data[1].heading1 == 2
    assert tree.data[1][0][0].heading1 == "2.1.1"
    assert tree.data[0].can_have_children() is True
    assert tree.data[0][0].can_have_children() is False
    assert tree.data[1][0].can_have_children() is True
    assert tree.data[1][1].can_have_children() is False
    assert tree.data[2].can_have_children() is False
    assert tree.data[3].can_have_children() is True
    assert tree.data[4].can_have_children() is True


##################
# Check that the tree accessors connect to the data
##################


def _check_data_access(tree):
    assert getattr(tree.data[0], tree._accessors[0]) == "one"
    assert getattr(tree.data[0], tree._accessors[1]) == 1


def test_constructor_without_data_nor_headings_nor_accessors():
    "A tree cannot be created without data, headings, accessors"
    with pytest.raises(ValueError):
        _ = toga.Tree()


# mysource_data
##################


def test_constructor_with_source_data(
    mysource_headings, mysource_accessors, mysource_data
):
    "A tree can be created with custom Source data, headings, accessors"
    tree = toga.Tree(
        headings=mysource_headings, data=mysource_data, accessors=mysource_accessors
    )
    _check_data_access(tree)


def test_constructor_with_source_data_without_headings(
    mysource_accessors, mysource_data
):
    "A tree can be created with custom Source data, accessors, without headings"
    tree = toga.Tree(data=mysource_data, accessors=mysource_accessors)
    _check_data_access(tree)


def test_constructor_with_source_data_with_headings_without_accessors(
    mysource_headings, mysource_data
):
    "A tree can be created with custom Source data, with headings, without accessors"
    tree = toga.Tree(headings=mysource_headings, data=mysource_data)
    with pytest.raises(AttributeError):
        # unfortunately, the headings do not match the data
        _check_data_access(tree)


def test_constructor_with_source_data_without_headings_nor_accessors(mysource_data):
    "A tree cannot be created with custom Source data, without headings, accessors"
    with pytest.raises(ValueError):
        _ = toga.Tree(data=mysource_data)


def test_data_setter_with_source_data(
    mysource_headings, mysource_accessors, mysource_data
):
    "A custom Source can be assigned to .data on a tree with accessors, headings"
    tree = toga.Tree(headings=mysource_headings, accessors=mysource_accessors)
    tree.data = mysource_data
    _check_data_access(tree)


def test_data_setter_with_source_data_without_headings(
    mysource_accessors, mysource_data
):
    "A custom Source can be assigned to .data on a tree with accessors, without headings"
    tree = toga.Tree(accessors=mysource_accessors)
    tree.data = mysource_data
    _check_data_access(tree)


def test_data_setter_with_source_data_with_headings_without_accessors(
    mysource_headings, mysource_data
):
    "A custom Source data cannot be assigned to .data on a tree without accessors"
    tree = toga.Tree(headings=mysource_headings)
    tree.data = mysource_data
    with pytest.raises(AttributeError):
        _check_data_access(tree)


# treesource_data
##################


def test_constructor_with_treesource_data(headings, accessors, treesource_data):
    "A tree can be created with TreeSource data, headings, accessors"
    tree = toga.Tree(headings=headings, data=treesource_data, accessors=accessors)
    _check_data_access(tree)


def test_constructor_with_treesource_data_without_accessors(headings, treesource_data):
    "A tree can be created with TreeSource data, headings, without accessors"
    tree = toga.Tree(headings=headings, data=treesource_data)
    with pytest.raises(AttributeError):
        # unfortunately, the headings do not match the data
        _check_data_access(tree)


def test_constructor_with_treesource_data_without_headings(accessors, treesource_data):
    "A tree can be created with TreeSource data, accessors, without headings"
    tree = toga.Tree(data=treesource_data, accessors=accessors)
    _check_data_access(tree)


def test_constructor_with_treesource_data_without_headings_nor_accessors(
    treesource_data,
):
    "A tree cannot be created with TreeSource data, without headings, accessors"
    with pytest.raises(ValueError):
        _ = toga.Tree(data=treesource_data)


def test_data_setter_with_treesource_data(headings, accessors, treesource_data):
    "A TreeSource can be assigned to .data on a tree with accessors, headings"
    tree = toga.Tree(headings=headings, accessors=accessors)
    tree.data = treesource_data
    _check_data_access(tree)


def test_data_setter_with_treesource_data_without_accessors(headings, treesource_data):
    "A TreeSource can be assigned to .data on a tree with headings, without accessors"
    tree = toga.Tree(headings=headings)
    tree.data = treesource_data
    with pytest.raises(AttributeError):
        # unfortunately, the headings do not match the data
        _check_data_access(tree)


def test_data_setter_with_treesource_data_without_headings(accessors, treesource_data):
    "A TreeSource can be assigned to .data on a tree with accessors, without headings"
    tree = toga.Tree(accessors=accessors)
    tree.data = treesource_data
    _check_data_access(tree)


# dict_data
##################


def test_constructor_with_dict_data(headings, accessors, dict_data):
    "A tree can be created with dict data, headings, accessors"
    tree = toga.Tree(headings=headings, data=dict_data, accessors=accessors)
    _check_data_access(tree)


def test_constructor_with_dict_data_without_accessors(headings, dict_data):
    "A tree can be created with dict data, headings, without accessors"
    tree = toga.Tree(headings=headings, data=dict_data)
    _check_data_access(tree)
    # accessors are derived from headings
    assert tree._accessors[0] == "heading_0"


def test_constructor_with_dict_data_without_headings(accessors, dict_data):
    "A tree can be created with dict data, accessors, without headings"
    tree = toga.Tree(data=dict_data, accessors=accessors)
    _check_data_access(tree)


def test_constructor_with_dict_data_without_headings_nor_accessors(dict_data):
    "A tree can be created with dict data, without accessors, headings"
    tree = toga.Tree(data=dict_data)
    _check_data_access(tree)
    # accessors are syntesized
    with pytest.raises(AttributeError):
        _ = tree.data[0].heading0
    with pytest.raises(AttributeError):
        _ = tree.data[0].heading_0


def test_data_setter_with_dict_data(headings, accessors, dict_data):
    "A dict can be assigned to .data on a tree with accessors, headings"
    tree = toga.Tree(headings=headings, accessors=accessors)
    tree.data = dict_data
    _check_data_access(tree)


def test_data_setter_with_dict_data_without_accessors(headings, dict_data):
    "A dict can be assigned to .data on a tree with headings, without accessors"
    tree = toga.Tree(headings=headings)
    tree.data = dict_data
    _check_data_access(tree)
    # accessors are derived from headings
    assert tree._accessors[0] == "heading_0"


def test_data_setter_with_dict_data_without_headings(accessors, dict_data):
    "A dict can be assigned to .data on a tree with accessors, without headings"
    tree = toga.Tree(accessors=accessors)
    tree.data = dict_data
    _check_data_access(tree)


# list_data / tuple_data
##################


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_constructor_with_list_data(headings, accessors, data, request):
    "A tree can be created with list or tuple data, headings, accessors"
    tree = toga.Tree(
        headings=headings, data=request.getfixturevalue(data), accessors=accessors
    )
    _check_data_access(tree)


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_constructor_with_list_data_without_accessors(headings, data, request):
    "A tree can be created with list or tuple data, headings, without accessors"
    tree = toga.Tree(headings=headings, data=request.getfixturevalue(data))
    _check_data_access(tree)
    # accessors are derived from headings
    assert tree._accessors[0] == "heading_0"


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_constructor_with_list_data_without_headings(accessors, data, request):
    "A tree can be created with list or tuple data, accessors, without headings"
    tree = toga.Tree(data=request.getfixturevalue(data), accessors=accessors)
    _check_data_access(tree)


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_constructor_with_list_data_without_headings_nor_accessors(data, request):
    "A tree can be created with list or tuple data, without accessors, headings"
    tree = toga.Tree(data=request.getfixturevalue(data))
    _check_data_access(tree)
    # accessors are syntesized
    with pytest.raises(AttributeError):
        _ = tree.data[0].heading0
    with pytest.raises(AttributeError):
        _ = tree.data[0].heading_0


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_data_setter_with_list_data(headings, accessors, data, request):
    "A list or tuple can be assigned to .data on a tree with accessors, headings"
    tree = toga.Tree(headings=headings, accessors=accessors)
    tree.data = request.getfixturevalue(data)
    _check_data_access(tree)


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_data_setter_with_list_data_without_accessors(headings, data, request):
    "A list or tuple can be assigned to .data on a tree with headings, without accessors"
    tree = toga.Tree(headings=headings)
    tree.data = request.getfixturevalue(data)
    _check_data_access(tree)
    # accessors are derived from headings
    assert tree._accessors[0] == "heading_0"


@pytest.mark.parametrize("data", ["list_data", "tuple_data"])
def test_data_setter_with_list_data_without_headings(accessors, data, request):
    "A list or tuple can be assigned to .data on a tree with accessors, without headings"
    tree = toga.Tree(accessors=accessors)
    tree.data = request.getfixturevalue(data)
    _check_data_access(tree)
