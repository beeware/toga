from android.view import View
from android.widget import FrameLayout, LinearLayout, TextView
from travertino.size import at_least

from toga.colors import TRANSPARENT

try:
    from com.google.android.material.card import MaterialCardView
except ImportError:  # pragma: no cover
    # Older projects that don't include the Material library. Can't be validated
    # in CI, so it's marked no-cover.
    MaterialCardView = None

from toga_android.colors import native_color

from ..container import Container
from .base import Widget


class Frame(Widget, Container):
    """A grouping container rendered as a Material card.

    The card *is* the widget's native view; a vertical LinearLayout inside it
    stacks an optional title above the content host (a RelativeLayout managed by
    Container).
    """

    def create(self):
        if MaterialCardView is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import MaterialCardView. Ensure that the Material "
                "system package (com.google.android.material:material:1.12.0) "
                "is listed in your app's dependencies."
            )
        self.native = MaterialCardView(self._native_activity)
        # A little inset so content doesn't sit flush against the rounded edge.
        pad = int(8 * self._native_activity.getResources().getDisplayMetrics().density)
        self.native.setContentPadding(pad, pad, pad, pad)

        # Vertical stack inside the card: optional title, then the content host.
        # MaterialCardView is a FrameLayout subclass, so its child uses
        # FrameLayout.LayoutParams.
        self.native_layout = LinearLayout(self._native_activity)
        self.native_layout.setOrientation(LinearLayout.VERTICAL)
        self.native.addView(
            self.native_layout,
            FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT,
            ),
        )

        # Title: GONE until set, so an empty title consumes no vertical space.
        self.native_title = TextView(self._native_activity)
        self.native_title.setVisibility(View.GONE)
        self.native_layout.addView(
            self.native_title,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT,
                0,  # weight 0: title takes only the height it needs
            ),
        )

        # Content host (a RelativeLayout) added into the LinearLayout.
        self.init_container(self.native_layout)
        self.native_content.setLayoutParams(
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT,
                1,  # weight 1: content expands to fill the remaining card space
            )
        )

    # set_content / clear_content are inherited from Container.

    def get_title(self):
        return str(self.native_title.getText())

    def set_title(self, title):
        if title:
            self.native_title.setText(title)
            self.native_title.setVisibility(View.VISIBLE)
        else:
            self.native_title.setText("")
            self.native_title.setVisibility(View.GONE)

    def set_background_color(self, color):
        # The base implementation would replace the card's background drawable
        # (destroying its rounded/elevated rendering). For the default TRANSPARENT,
        # keep the card's native surface; otherwise recolor via the card API.
        if color in (None, TRANSPARENT):
            return
        self.native.setCardBackgroundColor(native_color(color))

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        lp = self.native.getLayoutParams()
        title_height = (
            self.native_title.getHeight()
            if self.native_title.getVisibility() == View.VISIBLE
            else 0
        )
        pad_h = (
            self.native.getContentPaddingLeft() + self.native.getContentPaddingRight()
        )
        pad_v = (
            self.native.getContentPaddingTop() + self.native.getContentPaddingBottom()
        )
        self.resize_content(lp.width - pad_h, lp.height - pad_v - title_height)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
