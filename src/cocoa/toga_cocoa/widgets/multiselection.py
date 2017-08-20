from colosseum import CSS

from .base import Widget
from ..libs import *
from ..utils import process_callback

from .box import Box
import toga


class MultiSelection(Box):
    def create(self):
        self.native = None
        self.constraints = None
        self.values = self.interface.defaults
        self.switches = []
        self.interface._children = []  # Allow the Widget to have children.
        self.interface.style = CSS()

        # Label above switches
        self.label = toga.Label('')
        # Switches for every choice
        self.box = toga.Box()
        for i, (choice, default) in enumerate(zip(self.interface.choices, self.values)):
            def callback(widget):
                if self.interface.on_select:
                    self.interface.on_select(self.interface)

            switch = toga.Switch(choice, is_on=default, on_toggle=callback)

            self.switches.append(switch)
            self.box.add(switch)

        self.interface.add(self.label)
        self.interface.add(self.box)

        self.rehint()

    def set_label(self, label):
        self.label.text = label

    def get_selected_items(self):
        return [switch.label for switch in self.switches if switch.is_on is True]

    def set_row(self, value):
        self.box.style.flex_direction = 'row' if value else 'column'

        if value:
            self.box.style.flex_direction = 'row'
            # some styling
            self.box.margin_top = -5
            for switch in self.switches:
                switch.style.margin_left = 8
                switch.style.margin_top = 0
        else:
            self.box.style.flex_direction = 'column'
            # some styling
            self.box.margin_top = -5
            for i, switch in enumerate(self.switches):
                switch.style.margin_left = 8
                if i > 0:
                    switch.style.margin_top = -8
        self.box.rehint()
        self.rehint()