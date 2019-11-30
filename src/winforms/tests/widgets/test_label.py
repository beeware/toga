import unittest

import toga


class TestWinformsLabel(unittest.TestCase):
    def setUp(self):
        self.label = toga.Label(None)

        # make a shortcut for easy use
        self.winforms_label = self.label._impl.native

        self.window = toga.Window()
        self.window.content = self.label

    def test_defaults(self):
        # In C# Winforms application in Visual Studio, default font for
        # labels is Microsoft Sans Serif 8.25pt / 10.957215px??
        # Toga, however, sets a default font at 12 px in toga.style.pack
        # >>> Pack.validated_property('font_size', choices=FONT_SIZE_CHOICES, initial=12)

        self.assertEqual("", self.winforms_label.Text)
        self.assertEqual(self.winforms_label.Font.FontFamily.GetName(0), 'Microsoft Sans Serif')
        # self.assertEqual(self.winforms_label.Font.Size, 10.9572) TODO: This should be correct
        self.assertEqual(self.winforms_label.Font.Size, 12)
        self.assertEqual(self.winforms_label.Font.Bold, False)
        self.assertEqual(self.winforms_label.Font.Italic, False)
        self.assertEqual(self.winforms_label.Size.Width, 640)
        self.assertEqual(self.winforms_label.Size.Height, 23)

    def test_set_text(self):
        test_text = "Test Text"
        test_int_text = 1

        self.label.text = test_text
        self.assertEqual(test_text, self.winforms_label.Text)

        self.label.text = None
        self.assertEqual("", self.winforms_label.Text)

        self.label.text = test_int_text
        self.assertEqual(str(test_int_text), self.winforms_label.Text)

    def test_font(self):
        default_win_label_font = self.winforms_label.Font

        self.assertEqual(default_win_label_font.Size, 12.0)
        print('Size in points: ', default_win_label_font.SizeInPoints)
        print('Font size units: ', default_win_label_font.Unit)
        self.assertEqual(default_win_label_font.FontFamily.GetName(0), 'Microsoft Sans Serif')

        self.label.style.update(font_family='Arial', font_size=15)
        self.assertEqual(self.winforms_label.Font.FontFamily.GetName(0), 'Arial')
        self.assertEqual(self.winforms_label.Font.Size, 15)
        self.assertEqual(self.winforms_label.Font.Bold, False)

        self.label.style.update(font_family="Nonexisting Font", font_size=1, font_weight='bold', font_style='italic')
        self.assertEqual(self.winforms_label.Font.FontFamily.GetName(0), 'Microsoft Sans Serif')
        self.assertEqual(self.winforms_label.Font.Size, 1)
        self.assertEqual(self.winforms_label.Font.Bold, True)
        self.assertEqual(self.winforms_label.Font.Italic, True)

        # TODO: test for italic

    def test_rehinting(self):
        self.assertEqual(self.winforms_label.Text, "")
        self.assertEqual(self.winforms_label.Size.Width, 640)
        self.assertEqual(self.winforms_label.Size.Height, 23)
        self.label.text = "Long string of text"
        self.label.refresh()
        self.assertEqual(self.winforms_label.Size.Width, 640)
        self.assertEqual(self.winforms_label.Size.Height, 24)
