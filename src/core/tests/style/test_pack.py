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

        # HiDPI normal size
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

    def test_alignment_with_padding(self):
        root = TestNode(
            'app', style=Pack(), children=[
                TestNode('row_e_box', style=Pack(direction=COLUMN), children=[
                    TestNode('top_alignment_row_box', style=Pack(direction=ROW, alignment=TOP), children=[
                        TestNode('row_top_stretched', style=Pack(
                            height=120, width=30, padding_top=0, padding_bottom=0)),
                        TestNode('row_top_padded_0', style=Pack(
                            height=30, width=30, padding_top=0, padding_bottom=0)),
                        TestNode('row_top_padded_1', style=Pack(
                            height=30, width=30, padding_top=30, padding_bottom=0)),
                        TestNode('row_top_padded_2', style=Pack(
                            height=30, width=30, padding_top=0, padding_bottom=30)),
                        TestNode('row_top_padded_3', style=Pack(
                            height=30, width=30, padding_top=30, padding_bottom=30)),
                    ]),
                    TestNode('center_alignment_row_box', style=Pack(direction=ROW, alignment=CENTER), children=[
                        TestNode('row_center_stretched', style=Pack(
                            height=120, width=30, padding_top=0, padding_bottom=0)),
                        TestNode('row_center_padded_0', style=Pack(
                            height=30, width=30, padding_top=0, padding_bottom=0)),
                        TestNode('row_center_padded_1', style=Pack(
                            height=30, width=30, padding_top=30, padding_bottom=0)),
                        TestNode('row_center_padded_2', style=Pack(
                            height=30, width=30, padding_top=0, padding_bottom=30)),
                        TestNode('row_center_padded_3', style=Pack(
                            height=30, width=30, padding_top=30, padding_bottom=30)),
                    ]),
                    TestNode('bottom_alignment_row_box', style=Pack(direction=ROW, alignment=BOTTOM), children=[
                        TestNode('row_bottom_stretched', style=Pack(
                            height=120, width=30, padding_top=0, padding_bottom=0)),
                        TestNode('row_bottom_padded_0', style=Pack(
                            height=30, width=30, padding_top=0, padding_bottom=0)),
                        TestNode('row_bottom_padded_1', style=Pack(
                            height=30, width=30, padding_top=30, padding_bottom=0)),
                        TestNode('row_bottom_padded_2', style=Pack(
                            height=30, width=30, padding_top=0, padding_bottom=30)),
                        TestNode('row_bottom_padded_3', style=Pack(
                            height=30, width=30, padding_top=30, padding_bottom=30)),
                    ]),
                ]),
                TestNode('spacer_between', style=Pack(width=30)),
                TestNode('column_e_box', style=Pack(direction=ROW), children=[
                    TestNode('left_alignment_column_box', style=Pack(direction=COLUMN, alignment=LEFT), children=[
                        TestNode('column_left_stretched', style=Pack(
                            width=120, height=30, padding_left=0, padding_right=0)),
                        TestNode('column_left_padded_0', style=Pack(
                            width=30, height=30, padding_left=0, padding_right=0)),
                        TestNode('column_left_padded_1', style=Pack(
                            width=30, height=30, padding_left=30, padding_right=0)),
                        TestNode('column_left_padded_2', style=Pack(
                            width=30, height=30, padding_left=0, padding_right=30)),
                        TestNode('column_left_padded_3', style=Pack(
                            width=30, height=30, padding_left=30, padding_right=30)),
                    ]),
                    TestNode('center_alignment_column_box', style=Pack(direction=COLUMN, alignment=CENTER), children=[
                        TestNode('column_center_stretched', style=Pack(
                            width=120, height=30, padding_left=0, padding_right=0)),
                        TestNode('column_center_padded_0', style=Pack(
                            width=30, height=30, padding_left=0, padding_right=0)),
                        TestNode('column_center_padded_1', style=Pack(
                            width=30, height=30, padding_left=30, padding_right=0)),
                        TestNode('column_center_padded_2', style=Pack(
                            width=30, height=30, padding_left=0, padding_right=30)),
                        TestNode('column_center_padded_3', style=Pack(
                            width=30, height=30, padding_left=30, padding_right=30)),
                    ]),
                    TestNode('right_alignment_column_box', style=Pack(direction=COLUMN, alignment=RIGHT), children=[
                        TestNode('column_right_stretched', style=Pack(
                            width=120, height=30, padding_left=0, padding_right=0)),
                        TestNode('column_right_padded_0', style=Pack(
                            width=30, height=30, padding_left=0, padding_right=0)),
                        TestNode('column_right_padded_1', style=Pack(
                            width=30, height=30, padding_left=30, padding_right=0)),
                        TestNode('column_right_padded_2', style=Pack(
                            width=30, height=30, padding_left=0, padding_right=30)),
                        TestNode('column_right_padded_3', style=Pack(
                            width=30, height=30, padding_left=30, padding_right=30)),
                    ]),
                ]),
                TestNode('spacer_after', style=Pack(width=30)),
            ]
        )

        # Minimum size
        root.style.layout(root, TestViewport(0, 0, dpi=96))
        self.assertLayout(
            root,
            (570, 360),
            {'origin': (0, 0), 'content': (570, 360), 'children': [
                {'origin': (0, 0), 'content': (150, 360), 'children': [
                    {'origin': (0, 0), 'content': (150, 120), 'children': [
                        {'origin': (0, 0), 'content': (30, 120)},
                        {'origin': (30, 0), 'content': (30, 30)},
                        {'origin': (60, 30), 'content': (30, 30)},
                        {'origin': (90, 0), 'content': (30, 30)},
                        {'origin': (120, 30), 'content': (30, 30)},
                    ]},
                    {'origin': (0, 120), 'content': (150, 120), 'children': [
                        {'origin': (0, 120), 'content': (30, 120)},
                        {'origin': (30, 165), 'content': (30, 30)},
                        {'origin': (60, 180), 'content': (30, 30)},
                        {'origin': (90, 150), 'content': (30, 30)},
                        {'origin': (120, 165), 'content': (30, 30)},
                    ]},
                    {'origin': (0, 240), 'content': (150, 120), 'children': [
                        {'origin': (0, 240), 'content': (30, 120)},
                        {'origin': (30, 330), 'content': (30, 30)},
                        {'origin': (60, 330), 'content': (30, 30)},
                        {'origin': (90, 300), 'content': (30, 30)},
                        {'origin': (120, 300), 'content': (30, 30)},
                    ]},
                ]},
                {'origin': (150, 0), 'content': (30, 0)},
                {'origin': (180, 0), 'content': (360, 150), 'children': [
                    {'origin': (180, 0), 'content': (120, 150), 'children': [
                        {'origin': (180, 0), 'content': (120, 30)},
                        {'origin': (180, 30), 'content': (30, 30)},
                        {'origin': (210, 60), 'content': (30, 30)},
                        {'origin': (180, 90), 'content': (30, 30)},
                        {'origin': (210, 120), 'content': (30, 30)},
                    ]},
                    {'origin': (300, 0), 'content': (120, 150), 'children': [
                        {'origin': (300, 0), 'content': (120, 30)},
                        {'origin': (345, 30), 'content': (30, 30)},
                        {'origin': (360, 60), 'content': (30, 30)},
                        {'origin': (330, 90), 'content': (30, 30)},
                        {'origin': (345, 120), 'content': (30, 30)},
                    ]},
                    {'origin': (420, 0), 'content': (120, 150), 'children': [
                        {'origin': (420, 0), 'content': (120, 30)},
                        {'origin': (510, 30), 'content': (30, 30)},
                        {'origin': (510, 60), 'content': (30, 30)},
                        {'origin': (480, 90), 'content': (30, 30)},
                        {'origin': (480, 120), 'content': (30, 30)},
                    ]},
                ]},
                {'origin': (540, 0), 'content': (30, 0)},
            ]}
        )

        # Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=96))
        self.assertLayout(
            root,
            (570, 480),
            {'origin': (0, 0), 'content': (570, 480), 'children': [
                {'origin': (0, 0), 'content': (150, 360), 'children': [
                    {'origin': (0, 0), 'content': (150, 120), 'children': [
                        {'origin': (0, 0), 'content': (30, 120)},
                        {'origin': (30, 0), 'content': (30, 30)},
                        {'origin': (60, 30), 'content': (30, 30)},
                        {'origin': (90, 0), 'content': (30, 30)},
                        {'origin': (120, 30), 'content': (30, 30)},
                    ]},
                    {'origin': (0, 120), 'content': (150, 120), 'children': [
                        {'origin': (0, 120), 'content': (30, 120)},
                        {'origin': (30, 165), 'content': (30, 30)},
                        {'origin': (60, 180), 'content': (30, 30)},
                        {'origin': (90, 150), 'content': (30, 30)},
                        {'origin': (120, 165), 'content': (30, 30)},
                    ]},
                    {'origin': (0, 240), 'content': (150, 120), 'children': [
                        {'origin': (0, 240), 'content': (30, 120)},
                        {'origin': (30, 330), 'content': (30, 30)},
                        {'origin': (60, 330), 'content': (30, 30)},
                        {'origin': (90, 300), 'content': (30, 30)},
                        {'origin': (120, 300), 'content': (30, 30)},
                    ]},
                ]},
                {'origin': (150, 0), 'content': (30, 480)},
                {'origin': (180, 0), 'content': (360, 150), 'children': [
                    {'origin': (180, 0), 'content': (120, 150), 'children': [
                        {'origin': (180, 0), 'content': (120, 30)},
                        {'origin': (180, 30), 'content': (30, 30)},
                        {'origin': (210, 60), 'content': (30, 30)},
                        {'origin': (180, 90), 'content': (30, 30)},
                        {'origin': (210, 120), 'content': (30, 30)},
                    ]},
                    {'origin': (300, 0), 'content': (120, 150), 'children': [
                        {'origin': (300, 0), 'content': (120, 30)},
                        {'origin': (345, 30), 'content': (30, 30)},
                        {'origin': (360, 60), 'content': (30, 30)},
                        {'origin': (330, 90), 'content': (30, 30)},
                        {'origin': (345, 120), 'content': (30, 30)},
                    ]},
                    {'origin': (420, 0), 'content': (120, 150), 'children': [
                        {'origin': (420, 0), 'content': (120, 30)},
                        {'origin': (510, 30), 'content': (30, 30)},
                        {'origin': (510, 60), 'content': (30, 30)},
                        {'origin': (480, 90), 'content': (30, 30)},
                        {'origin': (480, 120), 'content': (30, 30)},
                    ]},
                ]},
                {'origin': (540, 0), 'content': (30, 480)},
            ]}
        )

        # HiDPI Normal size
        root.style.layout(root, TestViewport(640, 480, dpi=144))
        self.assertLayout(
            root,
            (855, 540),
            {'origin': (0, 0), 'content': (855, 540), 'children': [
                {'origin': (0, 0), 'content': (225, 540), 'children': [
                    {'origin': (0, 0), 'content': (225, 180), 'children': [
                        {'origin': (0, 0), 'content': (45, 180)},
                        {'origin': (45, 0), 'content': (45, 45)},
                        {'origin': (90, 45), 'content': (45, 45)},
                        {'origin': (135, 0), 'content': (45, 45)},
                        {'origin': (180, 45), 'content': (45, 45)},
                    ]},
                    {'origin': (0, 180), 'content': (225, 180), 'children': [
                        {'origin': (0, 180), 'content': (45, 180)},
                        {'origin': (45, 247), 'content': (45, 45)},
                        {'origin': (90, 270), 'content': (45, 45)},
                        {'origin': (135, 225), 'content': (45, 45)},
                        {'origin': (180, 247), 'content': (45, 45)},
                    ]},
                    {'origin': (0, 360), 'content': (225, 180), 'children': [
                        {'origin': (0, 360), 'content': (45, 180)},
                        {'origin': (45, 495), 'content': (45, 45)},
                        {'origin': (90, 495), 'content': (45, 45)},
                        {'origin': (135, 450), 'content': (45, 45)},
                        {'origin': (180, 450), 'content': (45, 45)},
                    ]},
                ]},
                {'origin': (225, 0), 'content': (45, 480)},
                {'origin': (270, 0), 'content': (540, 225), 'children': [
                    {'origin': (270, 0), 'content': (180, 225), 'children': [
                        {'origin': (270, 0), 'content': (180, 45)},
                        {'origin': (270, 45), 'content': (45, 45)},
                        {'origin': (315, 90), 'content': (45, 45)},
                        {'origin': (270, 135), 'content': (45, 45)},
                        {'origin': (315, 180), 'content': (45, 45)},
                    ]},
                    {'origin': (450, 0), 'content': (180, 225), 'children': [
                        {'origin': (450, 0), 'content': (180, 45)},
                        {'origin': (517, 45), 'content': (45, 45)},
                        {'origin': (540, 90), 'content': (45, 45)},
                        {'origin': (495, 135), 'content': (45, 45)},
                        {'origin': (517, 180), 'content': (45, 45)},
                    ]},
                    {'origin': (630, 0), 'content': (180, 225), 'children': [
                        {'origin': (630, 0), 'content': (180, 45)},
                        {'origin': (765, 45), 'content': (45, 45)},
                        {'origin': (765, 90), 'content': (45, 45)},
                        {'origin': (720, 135), 'content': (45, 45)},
                        {'origin': (720, 180), 'content': (45, 45)},
                    ]},
                ]},
                {'origin': (810, 0), 'content': (45, 480)},
            ]}
        )
