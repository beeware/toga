from unittest import TestCase
from unittest.mock import Mock

from travertino.node import Node
from travertino.size import at_least

from toga.colors import rgb
from toga.fonts import Font
from toga.style.applicator import TogaApplicator
from toga.style.pack import BOTTOM, CENTER, COLUMN, HIDDEN, LEFT, RIGHT, ROW, RTL, Pack, TOP


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


class TestViewport:
    def __init__(self, width, height, dpi=96, baseline_dpi=96):
        self.height = height
        self.width = width
        self.dpi = dpi
        self.baseline_dpi = baseline_dpi


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
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (220, 130),
            {'origin': (0, 0), 'content': (220, 130), 'children': [
                {'origin': (50, 50), 'content': (120, 30)}
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (640, 130),
            {'origin': (0, 0), 'content': (640, 130), 'children': [
                {'origin': (50, 50), 'content': (540, 30)}
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (640, 180),
            {'origin': (0, 0), 'content': (640, 180), 'children': [
                {'origin': (75, 75), 'content': (490, 30)}
            ]}
        )

    def test_tutorial_0_vertical(self):
        root = TestNode(
            'app', style=Pack(direction=COLUMN), children=[
                # TestNode('button', style=Pack(flex=1), size=(30, at_least(120))),
                TestNode('button', style=Pack(flex=1, padding=50), size=(30, at_least(120))),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (130, 220),
            {'origin': (0, 0), 'content': (130, 220), 'children': [
                {'origin': (50, 50), 'content': (30, 120)}
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(480, 640, dpi=96))
        self.assertLayout(
            root,
            (130, 640),
            {'origin': (0, 0), 'content': (130, 640), 'children': [
                {'origin': (50, 50), 'content': (30, 540)}
            ]}
        )

        # HiDPI normal size
        root.style.layout(root, TestViewport(480, 640, dpi=144))
        self.assertLayout(
            root,
            (180, 640),
            {'origin': (0, 0), 'content': (180, 640), 'children': [
                {'origin': (75, 75), 'content': (30, 490)}
            ]}
        )

    def test_tutorial_0_high_baseline_dpi(self):
        root = TestNode(
            'app', style=Pack(), children=[
                TestNode('button', style=Pack(flex=1, padding=50), size=(at_least(120), 30)),
            ]
        )

        # Minimum size with high baseline DPI
        root.style.layout(root, TestViewport(0, 0, dpi=160, baseline_dpi=160))
        self.assertLayout(
            root,
            (220, 130),
            {'origin': (0, 0), 'content': (220, 130), 'children': [
                {'origin': (50, 50), 'content': (120, 30)}
            ]}
        )

        # Normal size with high DPI equal to high baseline DPI
        root.style.layout(root, TestViewport(640, 480, dpi=160, baseline_dpi=160))
        self.assertLayout(
            root,
            (640, 130),
            {'origin': (0, 0), 'content': (640, 130), 'children': [
                {'origin': (50, 50), 'content': (540, 30)}
            ]}
        )

        # HiDPI -- 1.5x baseline -- with higher baseline DPI
        root.style.layout(root, TestViewport(640, 480, dpi=240, baseline_dpi=160))
        self.assertLayout(
            root,
            (640, 180),
            {'origin': (0, 0), 'content': (640, 180), 'children': [
                {'origin': (75, 75), 'content': (490, 30)}
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
        root.style.layout(root, TestViewport(0, 0, dpi=96))
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
        root.style.layout(root, TestViewport(640, 480, dpi=96))
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

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (640, 142),
            {'origin': (0, 10), 'content': (640, 132), 'children': [
                {'origin': (7, 17), 'content': (626, 15), 'children': [
                    {'origin': (247, 17), 'content': (221, 15)},
                    {'origin': (483, 17), 'content': (150, 10)},
                ]},
                {'origin': (7, 46), 'content': (626, 15), 'children': [
                    {'origin': (7, 46), 'content': (225, 10)},
                    {'origin': (247, 46), 'content': (221, 15)},
                    {'origin': (483, 46), 'content': (150, 10)},
                ]},
                {'origin': (22, 90), 'content': (596, 30)}
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
        root.style.layout(root, TestViewport(0, 0, dpi=96))
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
        root.style.layout(root, TestViewport(640, 480, dpi=96))
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

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (640, 480),
            {'origin': (0, 0), 'content': (640, 480), 'children': [
                {'origin': (0, 0), 'content': (640, 29), 'children': [
                    {'origin': (7, 7), 'content': (537, 15)},
                    {'origin': (558, 7), 'content': (75, 10)},
                ]},
                {'origin': (0, 29), 'content': (640, 451)}
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
        root.style.layout(root, TestViewport(0, 0, dpi=96))
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
        root.style.layout(root, TestViewport(640, 480, dpi=96))
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

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (640, 480),
            {'origin': (0, 0), 'content': (640, 480), 'children': [
                {'origin': (0, 0), 'content': (640, 451)},
                {'origin': (0, 451), 'content': (640, 29), 'children': [
                    {'origin': (7, 458), 'content': (572, 15)},
                    {'origin': (593, 458), 'content': (40, 10)},
                ]},
            ]}
        )

    def test_row_alignment_top(self):
        root = TestNode(
            'root', style=Pack(direction=ROW, alignment=TOP, width=300), children=[
                TestNode('space_filler', style=Pack(width=100, height=540)),
                TestNode('container', style=Pack(direction=COLUMN, padding_top=110, padding_bottom=120), children=[
                    TestNode('widget_a', style=Pack(height=30, padding_top=32, padding_bottom=34)),
                    TestNode('widget_b', style=Pack(height=36, padding_top=38, padding_bottom=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 110), 'content': (200, 210), 'children': [
                    {'origin': (100, 142), 'content': (200, 30)},
                    {'origin': (100, 244), 'content': (200, 36)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 110), 'content': (200, 210), 'children': [
                    {'origin': (100, 142), 'content': (200, 30)},
                    {'origin': (100, 244), 'content': (200, 36)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (450, 810),
            {'origin': (0, 0), 'content': (450, 810), 'children': [
                {'origin': (0, 0), 'content': (150, 810)},
                {'origin': (150, 165), 'content': (300, 315), 'children': [
                    {'origin': (150, 213), 'content': (300, 45)},
                    {'origin': (150, 366), 'content': (300, 54)},
                ]}
            ]}
        )

    def test_row_alignment_center(self):
        root = TestNode(
            'root', style=Pack(direction=ROW, alignment=CENTER, width=300), children=[
                TestNode('space_filler', style=Pack(width=100, height=540)),
                TestNode('container', style=Pack(direction=COLUMN, padding_top=110, padding_bottom=120), children=[
                    TestNode('widget_a', style=Pack(height=30, padding_top=32, padding_bottom=34)),
                    TestNode('widget_b', style=Pack(height=36, padding_top=38, padding_bottom=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 160), 'content': (200, 210), 'children': [
                    {'origin': (100, 192), 'content': (200, 30)},
                    {'origin': (100, 294), 'content': (200, 36)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 160), 'content': (200, 210), 'children': [
                    {'origin': (100, 192), 'content': (200, 30)},
                    {'origin': (100, 294), 'content': (200, 36)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (450, 810),
            {'origin': (0, 0), 'content': (450, 810), 'children': [
                {'origin': (0, 0), 'content': (150, 810)},
                {'origin': (150, 240), 'content': (300, 315), 'children': [
                    {'origin': (150, 288), 'content': (300, 45)},
                    {'origin': (150, 441), 'content': (300, 54)},
                ]}
            ]}
        )

    def test_row_alignment_bottom(self):
        root = TestNode(
            'root', style=Pack(direction=ROW, alignment=BOTTOM, width=300), children=[
                TestNode('space_filler', style=Pack(width=100, height=540)),
                TestNode('container', style=Pack(direction=COLUMN, padding_top=110, padding_bottom=120), children=[
                    TestNode('widget_a', style=Pack(height=30, padding_top=32, padding_bottom=34)),
                    TestNode('widget_b', style=Pack(height=36, padding_top=38, padding_bottom=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 210), 'content': (200, 210), 'children': [
                    {'origin': (100, 242), 'content': (200, 30)},
                    {'origin': (100, 344), 'content': (200, 36)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 210), 'content': (200, 210), 'children': [
                    {'origin': (100, 242), 'content': (200, 30)},
                    {'origin': (100, 344), 'content': (200, 36)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (450, 810),
            {'origin': (0, 0), 'content': (450, 810), 'children': [
                {'origin': (0, 0), 'content': (150, 810)},
                {'origin': (150, 315), 'content': (300, 315), 'children': [
                    {'origin': (150, 363), 'content': (300, 45)},
                    {'origin': (150, 516), 'content': (300, 54)},
                ]}
            ]}
        )

    def test_column_alignment_left(self):
        root = TestNode(
            'root', style=Pack(direction=COLUMN, alignment=LEFT, height=300), children=[
                TestNode('space_filler', style=Pack(width=540, height=100)),
                TestNode('container', style=Pack(direction=ROW, padding_left=110, padding_right=120), children=[
                    TestNode('widget_a', style=Pack(width=30, padding_left=32, padding_right=34)),
                    TestNode('widget_b', style=Pack(width=36, padding_left=38, padding_right=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (110, 100), 'content': (210, 200), 'children': [
                    {'origin': (142, 100), 'content': (30, 200)},
                    {'origin': (244, 100), 'content': (36, 200)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (110, 100), 'content': (210, 200), 'children': [
                    {'origin': (142, 100), 'content': (30, 200)},
                    {'origin': (244, 100), 'content': (36, 200)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (810, 450),
            {'origin': (0, 0), 'content': (810, 450), 'children': [
                {'origin': (0, 0), 'content': (810, 150)},
                {'origin': (165, 150), 'content': (315, 300), 'children': [
                    {'origin': (213, 150), 'content': (45, 300)},
                    {'origin': (366, 150), 'content': (54, 300)},
                ]}
            ]}
        )

    def test_column_alignment_center(self):
        root = TestNode(
            'root', style=Pack(direction=COLUMN, alignment=CENTER, height=300), children=[
                TestNode('space_filler', style=Pack(width=540, height=100)),
                TestNode('container', style=Pack(direction=ROW, padding_left=110, padding_right=120), children=[
                    TestNode('widget_a', style=Pack(width=30, padding_left=32, padding_right=34)),
                    TestNode('widget_b', style=Pack(width=36, padding_left=38, padding_right=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (160, 100), 'content': (210, 200), 'children': [
                    {'origin': (192, 100), 'content': (30, 200)},
                    {'origin': (294, 100), 'content': (36, 200)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (160, 100), 'content': (210, 200), 'children': [
                    {'origin': (192, 100), 'content': (30, 200)},
                    {'origin': (294, 100), 'content': (36, 200)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (810, 450),
            {'origin': (0, 0), 'content': (810, 450), 'children': [
                {'origin': (0, 0), 'content': (810, 150)},
                {'origin': (240, 150), 'content': (315, 300), 'children': [
                    {'origin': (288, 150), 'content': (45, 300)},
                    {'origin': (441, 150), 'content': (54, 300)},
                ]}
            ]}
        )

    def test_column_alignment_right(self):
        root = TestNode(
            'root', style=Pack(direction=COLUMN, alignment=RIGHT, height=300), children=[
                TestNode('space_filler', style=Pack(width=540, height=100)),
                TestNode('container', style=Pack(direction=ROW, padding_left=110, padding_right=120), children=[
                    TestNode('widget_a', style=Pack(width=30, padding_left=32, padding_right=34)),
                    TestNode('widget_b', style=Pack(width=36, padding_left=38, padding_right=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (210, 100), 'content': (210, 200), 'children': [
                    {'origin': (242, 100), 'content': (30, 200)},
                    {'origin': (344, 100), 'content': (36, 200)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (210, 100), 'content': (210, 200), 'children': [
                    {'origin': (242, 100), 'content': (30, 200)},
                    {'origin': (344, 100), 'content': (36, 200)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (810, 450),
            {'origin': (0, 0), 'content': (810, 450), 'children': [
                {'origin': (0, 0), 'content': (810, 150)},
                {'origin': (315, 150), 'content': (315, 300), 'children': [
                    {'origin': (363, 150), 'content': (45, 300)},
                    {'origin': (516, 150), 'content': (54, 300)},
                ]}
            ]}
        )

    def test_row_alignment_no_padding(self):
        root = TestNode(
            'root', style=Pack(direction=ROW, alignment=CENTER, width=300), children=[
                TestNode('space_filler', style=Pack(width=100, height=540)),
                TestNode('widget', style=Pack(height=440)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 50), 'content': (200, 440)},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (300, 540),
            {'origin': (0, 0), 'content': (300, 540), 'children': [
                {'origin': (0, 0), 'content': (100, 540)},
                {'origin': (100, 50), 'content': (200, 440)},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (450, 810),
            {'origin': (0, 0), 'content': (450, 810), 'children': [
                {'origin': (0, 0), 'content': (150, 810)},
                {'origin': (150, 75), 'content': (300, 660)}
            ]}
        )

    def test_column_alignment_no_padding(self):
        root = TestNode(
            'root', style=Pack(direction=COLUMN, alignment=CENTER, height=300), children=[
                TestNode('space_filler', style=Pack(width=540, height=100)),
                TestNode('widget', style=Pack(width=440)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (50, 100), 'content': (440, 200)},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (540, 300),
            {'origin': (0, 0), 'content': (540, 300), 'children': [
                {'origin': (0, 0), 'content': (540, 100)},
                {'origin': (50, 100), 'content': (440, 200)},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (810, 450),
            {'origin': (0, 0), 'content': (810, 450), 'children': [
                {'origin': (0, 0), 'content': (810, 150)},
                {'origin': (75, 150), 'content': (660, 300)}
            ]}
        )

    def test_row_alignment_row_box(self):
        root = TestNode(
            'root', style=Pack(direction=ROW, alignment=CENTER), children=[
                TestNode('space_filler', style=Pack(width=100, height=430)),
                TestNode('container', style=Pack(direction=ROW, padding_top=110, padding_bottom=120), children=[
                    TestNode('widget_a', style=Pack(width=30, height=100, padding_left=32, padding_right=34)),
                    TestNode('widget_b', style=Pack(width=36, height=100, padding_left=38, padding_right=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (310, 430),
            {'origin': (0, 0), 'content': (310, 430), 'children': [
                {'origin': (0, 0), 'content': (100, 430)},
                {'origin': (100, 160), 'content': (210, 100), 'children': [
                    {'origin': (132, 160), 'content': (30, 100)},
                    {'origin': (234, 160), 'content': (36, 100)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (310, 430),
            {'origin': (0, 0), 'content': (310, 430), 'children': [
                {'origin': (0, 0), 'content': (100, 430)},
                {'origin': (100, 160), 'content': (210, 100), 'children': [
                    {'origin': (132, 160), 'content': (30, 100)},
                    {'origin': (234, 160), 'content': (36, 100)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (465, 645),
            {'origin': (0, 0), 'content': (465, 645), 'children': [
                {'origin': (0, 0), 'content': (150, 645)},
                {'origin': (150, 240), 'content': (315, 150), 'children': [
                    {'origin': (198, 240), 'content': (45, 150)},
                    {'origin': (351, 240), 'content': (54, 150)},
                ]},
            ]}
        )

    def test_column_alignment_column_box(self):
        root = TestNode(
            'root', style=Pack(direction=COLUMN, alignment=CENTER), children=[
                TestNode('space_filler', style=Pack(width=430, height=100)),
                TestNode('container', style=Pack(direction=COLUMN, padding_left=110, padding_right=120), children=[
                    TestNode('widget_a', style=Pack(width=100, height=30, padding_top=32, padding_bottom=34)),
                    TestNode('widget_b', style=Pack(width=100, height=36, padding_top=38, padding_bottom=40)),
                ]),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (430, 310),
            {'origin': (0, 0), 'content': (430, 310), 'children': [
                {'origin': (0, 0), 'content': (430, 100)},
                {'origin': (160, 100), 'content': (100, 210), 'children': [
                    {'origin': (160, 132), 'content': (100, 30)},
                    {'origin': (160, 234), 'content': (100, 36)},
                ]},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (430, 310),
            {'origin': (0, 0), 'content': (430, 310), 'children': [
                {'origin': (0, 0), 'content': (430, 100)},
                {'origin': (160, 100), 'content': (100, 210), 'children': [
                    {'origin': (160, 132), 'content': (100, 30)},
                    {'origin': (160, 234), 'content': (100, 36)},
                ]},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (645, 465),
            {'origin': (0, 0), 'content': (645, 465), 'children': [
                {'origin': (0, 0), 'content': (645, 150)},
                {'origin': (240, 150), 'content': (150, 315), 'children': [
                    {'origin': (240, 198), 'content': (150, 45)},
                    {'origin': (240, 351), 'content': (150, 54)},
                ]},
            ]}
        )

    def test_rtl_row_box_child_layout(self):
        root = TestNode(
            'container', style=Pack(text_direction=RTL, direction=ROW), children=[
                TestNode('widget_a', style=Pack(width=30, height=100, padding_left=32, padding_right=34)),
                TestNode('widget_b', style=Pack(width=36, height=100, padding_left=38, padding_right=40)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (210, 100),
            {'origin': (0, 0), 'content': (210, 100), 'children': [
                {'origin': (146, 0), 'content': (30, 100)},
                {'origin': (38, 0), 'content': (36, 100)},
            ]},
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (210, 100),
            {'origin': (0, 0), 'content': (210, 100), 'children': [
                {'origin': (146, 0), 'content': (30, 100)},
                {'origin': (38, 0), 'content': (36, 100)},
            ]},
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (315, 150),
            {'origin': (0, 0), 'content': (315, 150), 'children': [
                {'origin': (219, 0), 'content': (45, 150)},
                {'origin': (57, 0), 'content': (54, 150)},
            ]},
        )

    def test_rtl_column_box_child_layout(self):
        root = TestNode(
            'container', style=Pack(text_direction=RTL, direction=COLUMN), children=[
                TestNode('widget_a', style=Pack(width=100, height=30, padding_top=32, padding_bottom=34)),
                TestNode('widget_b', style=Pack(width=100, height=36, padding_top=38, padding_bottom=40)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (100, 210),
            {'origin': (0, 0), 'content': (100, 210), 'children': [
                {'origin': (0, 32), 'content': (100, 30)},
                {'origin': (0, 134), 'content': (100, 36)},
            ]},
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (100, 210),
            {'origin': (0, 0), 'content': (100, 210), 'children': [
                {'origin': (0, 32), 'content': (100, 30)},
                {'origin': (0, 134), 'content': (100, 36)},
            ]},
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (150, 315),
            {'origin': (0, 0), 'content': (150, 315), 'children': [
                {'origin': (0, 48), 'content': (150, 45)},
                {'origin': (0, 201), 'content': (150, 54)},
            ]},
        )

    def test_rtl_alignment_top(self):
        root = TestNode(
            'root', style=Pack(text_direction=RTL, direction=ROW, alignment=TOP), children=[
                TestNode('space_filler', style=Pack(width=30, height=100)),
                TestNode('widget', style=Pack(width=30, height=30)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (60, 100),
            {'origin': (0, 0), 'content': (60, 100), 'children': [
                {'origin': (30, 0), 'content': (30, 100)},
                {'origin': (0, 0), 'content': (30, 30)},
            ]},
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (60, 100),
            {'origin': (0, 0), 'content': (60, 100), 'children': [
                {'origin': (30, 0), 'content': (30, 100)},
                {'origin': (0, 0), 'content': (30, 30)},
            ]},
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (90, 150),
            {'origin': (0, 0), 'content': (90, 150), 'children': [
                {'origin': (45, 0), 'content': (45, 150)},
                {'origin': (0, 0), 'content': (45, 45)},
            ]},
        )

    def test_rtl_alignment_bottom(self):
        root = TestNode(
            'root', style=Pack(text_direction=RTL, direction=ROW, alignment=BOTTOM), children=[
                TestNode('space_filler', style=Pack(width=30, height=100)),
                TestNode('widget', style=Pack(width=30, height=30)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (60, 100),
            {'origin': (0, 0), 'content': (60, 100), 'children': [
                {'origin': (30, 0), 'content': (30, 100)},
                {'origin': (0, 70), 'content': (30, 30)},
            ]},
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (60, 100),
            {'origin': (0, 0), 'content': (60, 100), 'children': [
                {'origin': (30, 0), 'content': (30, 100)},
                {'origin': (0, 70), 'content': (30, 30)},
            ]},
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (90, 150),
            {'origin': (0, 0), 'content': (90, 150), 'children': [
                {'origin': (45, 0), 'content': (45, 150)},
                {'origin': (0, 105), 'content': (45, 45)},
            ]},
        )

    def test_rtl_alignment_left(self):
        root = TestNode(
            'root', style=Pack(text_direction=RTL, direction=COLUMN, alignment=LEFT), children=[
                TestNode('space_filler', style=Pack(width=100, height=30)),
                TestNode('widget', style=Pack(width=30, height=30)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (100, 60),
            {'origin': (0, 0), 'content': (100, 60), 'children': [
                {'origin': (0, 0), 'content': (100, 30)},
                {'origin': (0, 30), 'content': (30, 30)},
            ]},
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (100, 60),
            {'origin': (0, 0), 'content': (100, 60), 'children': [
                {'origin': (0, 0), 'content': (100, 30)},
                {'origin': (0, 30), 'content': (30, 30)},
            ]},
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (150, 90),
            {'origin': (0, 0), 'content': (150, 90), 'children': [
                {'origin': (0, 0), 'content': (150, 45)},
                {'origin': (0, 45), 'content': (45, 45)},
            ]},
        )

    def test_rtl_alignment_right(self):
        root = TestNode(
            'root', style=Pack(text_direction=RTL, direction=COLUMN, alignment=RIGHT), children=[
                TestNode('space_filler', style=Pack(width=100, height=30)),
                TestNode('widget', style=Pack(width=30, height=30)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (100, 60),
            {'origin': (0, 0), 'content': (100, 60), 'children': [
                {'origin': (0, 0), 'content': (100, 30)},
                {'origin': (70, 30), 'content': (30, 30)},
            ]},
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (100, 60),
            {'origin': (0, 0), 'content': (100, 60), 'children': [
                {'origin': (0, 0), 'content': (100, 30)},
                {'origin': (70, 30), 'content': (30, 30)},
            ]},
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (150, 90),
            {'origin': (0, 0), 'content': (150, 90), 'children': [
                {'origin': (0, 0), 'content': (150, 45)},
                {'origin': (105, 45), 'content': (45, 45)},
            ]},
        )
