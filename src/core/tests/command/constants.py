import toga

PARENT_GROUP1 = toga.Group("P", 1)
CHILD_GROUP1 = toga.Group("C", order=2, parent=PARENT_GROUP1)
CHILD_GROUP2 = toga.Group("B", order=4, parent=PARENT_GROUP1)
PARENT_GROUP2 = toga.Group("O", 2)
CHILD_GROUP3 = toga.Group("A", 2, parent=PARENT_GROUP2)

A = toga.Command(None, "A", group=PARENT_GROUP2, order=1)
S = toga.Command(None, "S", group=PARENT_GROUP1, order=5)
T = toga.Command(None, "T", group=CHILD_GROUP2, order=2)
U = toga.Command(None, "U", group=CHILD_GROUP2, order=1)
V = toga.Command(None, "V", group=PARENT_GROUP1, order=3)
B = toga.Command(None, "B", group=CHILD_GROUP1, section=2, order=1)
W = toga.Command(None, "W", group=CHILD_GROUP1, order=4)
X = toga.Command(None, "X", group=CHILD_GROUP1, order=2)
Y = toga.Command(None, "Y", group=CHILD_GROUP1, order=1)
Z = toga.Command(None, "Z", group=PARENT_GROUP1, order=1)

COMMANDS_IN_ORDER = [Z, Y, X, W, B, V, U, T, S, A]
COMMANDS_IN_SET = [
    Z, toga.GROUP_BREAK,
    Y, X, W, toga.SECTION_BREAK, B, toga.GROUP_BREAK,
    V, toga.GROUP_BREAK,
    U, T, toga.GROUP_BREAK,
    S, toga.GROUP_BREAK,
    A,
]
