from unittest import TestCase
from unittest.mock import Mock

from travertino.layout import Viewport
from travertino.node import Node
from travertino.size import at_least

from toga.colors import rgb
from toga.fonts import Font
from toga.style.pack import Pack, CENTER, COLUMN, HIDDEN, LEFT, RIGHT, ROW, RTL
from toga.style.applicator import TogaApplicator


class TestNode(Node):
    def __init__(self, name, style, size=None, children=None):
        super().__init__(style=style, children=children,
                         applicator=TogaApplicator(self))
        self.name = name
        self._impl = Mock()
        if size:
            self.intrinsic.width = size[0]
            self.intrinsic.height = size[1]

    def __repr__(self):
        return '<{} at {}>'.format(self.name, id(self))


class TestPackStyleApply(TestCase):

    def test_set_default_right_textalign_when_rtl(self):
        root = TestNode(
            'app', style=Pack(text_align=None, text_direction=RTL)
        )
        root.style.reapply()
        root._impl.set_alignment.assert_called_once_with(RIGHT)

    def test_set_default_left_textalign_when_no_rtl(self):
        root = TestNode(
            'app', style=Pack(text_align=None)
        )
        root.style.reapply()
        root._impl.set_alignment.assert_called_once_with(LEFT)

    def test_set_center_alignment(self):
        root = TestNode(
            'app', style=Pack(text_align='center')
        )
        root.style.reapply()
        root._impl.set_alignment.assert_called_once_with(CENTER)

    def test_set_color(self):
        color = '#ffffff'
        root = TestNode(
            'app', style=Pack(color=color)
        )
        root.style.reapply()
        root._impl.set_color.assert_called_once_with(rgb(255, 255, 255))

    def test_set_background_color(self):
        color = '#ffffff'
        root = TestNode(
            'app', style=Pack(background_color=color)
        )
        root.style.reapply()
        root._impl.set_background_color.assert_called_once_with(rgb(255, 255, 255))

    def test_set_font(self):
        root = TestNode(
            'app', style=Pack(font_family='Roboto',
                              font_size=12,
                              font_style='normal',
                              font_variant='small-caps',
                              font_weight='bold')
        )
        root.style.reapply()
        root._impl.set_font.assert_called_with(
            Font('Roboto', 12, 'normal', 'small-caps', 'bold')
        )

    def test_set_visibility_hidden(self):
        root = TestNode(
            'app', style=Pack(visibility=HIDDEN)
        )
        root.style.reapply()
        root._impl.set_hidden.assert_called_once_with(True)


class PackLayoutTests(TestCase):
    def assertLayout(self, node, size, layout):
        self.assertEqual(
            (node.layout.width, node.layout.height), size,
            "final size doesn't match"
        )
        self._assertLayout(node, layout)

    def _assertLayout(self, node, layout):
        self.assertEqual(
            (node.layout.absolute_content_left, node.layout.absolute_content_top),
            layout['origin'],
            "origin of {} doesn't match".format(node)
        )
        self.assertEqual(
            (node.layout.content_width, node.layout.content_height),
            layout['content'],
            "content of {} doesn't match".format(node)
        )

        self.assertEqual(
            len(node.children),
            len(layout.get('children', [])),
            "number of children of {} doesn't match".format(node)
        )

        for child, sublayout in zip(node.children, layout.get('children', [])):
            self._assertLayout(child, sublayout)

    def test_tutorial_0(self):
        root = TestNode(
            'app', style=Pack(), children=[
                TestNode('button', style=Pack(flex=1, padding=50), size=(at_least(120), 30)),
            ]
        )

        # Minimum size
        root.style.layout(root, Viewport(0, 0))
        self.assertLayout(
            root,
            (220, 130),
            {'origin': (0, 0), 'content': (220, 130), 'children': [
                {'origin': (50, 50), 'content': (120, 30)}
            ]}
        )

        # Normal size
        root.style.layout(root, Viewport(640, 480))
        self.assertLayout(
            root,
            (640, 130),
            {'origin': (0, 0), 'content': (640, 130), 'children': [
                {'origin': (50, 50), 'content': (540, 30)}
            ]}
        )

    def test_tutorial_1(self):
        root = TestNode(
            'app', style=Pack(direction=COLUMN, padding_top=10), children=[
                TestNode('f_box', style=Pack(direction=ROW, padding=5), children=[
                    TestNode('f_input', style=Pack(flex=1, padding_left=160), size=(at_least(100), 15)),
                    TestNode('f_label', style=Pack(width=100, padding_left=10), size=(at_least(40), 10)),
                ]),
                TestNode('c_box', style=Pack(direction=ROW, padding=5), children=[
                    TestNode('join_label', style=Pack(width=150, padding_right=10), size=(at_least(80), 10)),
                    TestNode('c_input', style=Pack(flex=1), size=(at_least(100), 15)),
                    TestNode('c_label', style=Pack(width=100, padding_left=10), size=(at_least(40), 10)),
                ]),
                TestNode('button', style=Pack(flex=1, padding=15), size=(at_least(120), 30)),
            ]
        )

        # Minimum size
        root.style.layout(root, Viewport(0, 0))
        self.assertLayout(
            root,
            (380, 120),
            {'origin': (0, 10), 'content': (380, 110), 'children': [
                {'origin': (5, 15), 'content': (370, 15), 'children': [
                    {'origin': (165, 15), 'content': (100, 15)},
                    {'origin': (275, 15), 'content': (100, 10)},
                ]},
                {'origin': (5, 40), 'content': (370, 15), 'children': [
                    {'origin': (5, 40), 'content': (150, 10)},
                    {'origin': (165, 40), 'content': (100, 15)},
                    {'origin': (275, 40), 'content': (100, 10)},
                ]},
                {'origin': (15, 75), 'content': (120, 30)}
            ]}
        )

        # Normal size
        root.style.layout(root, Viewport(640, 480))
        self.assertLayout(
            root,
            (640, 120),
            {'origin': (0, 10), 'content': (640, 110), 'children': [
                {'origin': (5, 15), 'content': (630, 15), 'children': [
                    {'origin': (165, 15), 'content': (360, 15)},
                    {'origin': (535, 15), 'content': (100, 10)},
                ]},
                {'origin': (5, 40), 'content': (630, 15), 'children': [
                    {'origin': (5, 40), 'content': (150, 10)},
                    {'origin': (165, 40), 'content': (360, 15)},
                    {'origin': (535, 40), 'content': (100, 10)},
                ]},
                {'origin': (15, 75), 'content': (610, 30)}
            ]}
        )

    def test_tutorial_3(self):
        root = TestNode(
            'app', style=Pack(direction=COLUMN), children=[
                TestNode('box', style=Pack(), children=[
                    TestNode('input', style=Pack(flex=1, padding=5), size=(at_least(100), 15)),
                    TestNode('button', style=Pack(width=50, padding=5), size=(at_least(40), 10)),
                ]),
                TestNode('web', style=Pack(flex=1), size=(at_least(100), at_least(100))),
            ]
        )

        # Minimum size
        root.style.layout(root, Viewport(0, 0))
        self.assertLayout(
            root,
            (170, 125),
            {'origin': (0, 0), 'content': (170, 125), 'children': [
                {'origin': (0, 0), 'content': (170, 25), 'children': [
                    {'origin': (5, 5), 'content': (100, 15)},
                    {'origin': (115, 5), 'content': (50, 10)},
                ]},
                {'origin': (0, 25), 'content': (100, 100)}
            ]}
        )

        # Normal size
        root.style.layout(root, Viewport(640, 480))
        self.assertLayout(
            root,
            (640, 480),
            {'origin': (0, 0), 'content': (640, 480), 'children': [
                {'origin': (0, 0), 'content': (640, 25), 'children': [
                    {'origin': (5, 5), 'content': (570, 15)},
                    {'origin': (585, 5), 'content': (50, 10)},
                ]},
                {'origin': (0, 25), 'content': (640, 455)}
            ]}
        )

    def test_beeliza(self):
        root = TestNode(
            'app', style=Pack(direction=COLUMN), children=[
                TestNode('detailedlist', style=Pack(flex=1), size=(at_least(100), at_least(100))),
                TestNode('box', style=Pack(direction=ROW), children=[
                    TestNode('input', style=Pack(flex=1, padding=5), size=(at_least(100), 15)),
                    TestNode('button', style=Pack(padding=5), size=(at_least(40), 10)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, Viewport(0, 0))
        self.assertLayout(
            root,
            (160, 125),
            {'origin': (0, 0), 'content': (160, 125), 'children': [
                {'origin': (0, 0), 'content': (100, 100)},
                {'origin': (0, 100), 'content': (160, 25), 'children': [
                    {'origin': (5, 105), 'content': (100, 15)},
                    {'origin': (115, 105), 'content': (40, 10)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, Viewport(640, 480))
        self.assertLayout(
            root,
            (640, 480),
            {'origin': (0, 0), 'content': (640, 480), 'children': [
                {'origin': (0, 0), 'content': (640, 455)},
                {'origin': (0, 455), 'content': (640, 25), 'children': [
                    {'origin': (5, 460), 'content': (580, 15)},
                    {'origin': (595, 460), 'content': (40, 10)},
                ]},
            ]}
        )
