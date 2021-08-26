from travertino.size import at_least
from rubicon.java import JavaClass
from ..libs.activity import MainActivity
from ..libs.android import R__attr
from ..libs.android.util import AttributeSet, Xml
from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.widget import (
    ProgressBar as A_ProgressBar,
    LinearLayout,
    LinearLayout__LayoutParams
)
from .base import Widget

class ProgressBar(Widget):
    def create(self):
        # progressBar = new ProgressBar(youractivity.this, null, android.R.attr.progressBarStyleLarge);
        # progressbar = A_ProgressBar(self._native_activity, attr_set, R__attr.progressBarStyleHorizontal)
        # progressbar = A_ProgressBar(self._native_activity, attr_set, R__attr.progressBarStyleLarge)
        # progressBar = A_ProgressBar(self._native_activity, None, R__attr.progressBarStyleLarge)

        # create an AttributeSet from a xml string
        xml_attrs = f'''<ProgressBar xmlns:android="http://schemas.android.com/apk/res/android"
            android:layout_width="fill_parent"
            android:layout_height="wrap_content"
            style = "@android:style/Widget.ProgressBar.Horizontal" />
        '''
        StringReader = JavaClass("java/io/StringReader")
        reader = StringReader(xml_attrs)
        XmlPullParser = JavaClass("org/xmlpull/v1/XmlPullParser")
        parser = Xml.newPullParser()
        parser.setInput(reader)
        attrs = Xml.asAttributeSet(parser)
        eventtype = parser.next()
        while eventtype != XmlPullParser.START_TAG and eventtype != XmlPullParser.END_DOCUMENT:
            eventtype = parser.next()
        # create instance of ProgressBar
        print('SIZE OF ATTRIBUTESET: '+str(attrs.getAttributeCount()))
        for i in range(0,attrs.getAttributeCount()):
            print('Attribute: '+attrs.getAttributeName(i)+"="+attrs.getAttributeValue(i))
        progressbar = A_ProgressBar(self._native_activity, attrs)
        self.native = progressbar

    def start(self):
        self.set_running_style()

    def stop(self):
        self.set_stopping_style()

    @property
    def max(self):
        return self.interface.max

    def set_max(self, value):
        if value is not None:
            self.native.setMax(int(value))
        if self.interface.is_running:
            self.set_running_style()
        else:
            self.set_stopping_style()

    def set_running_style(self):
        if self.max is None:
            self.native.setIndeterminate(True)
        else:
            self.native.setIndeterminate(False)

    def set_stopping_style(self):
        self.native.setIndeterminate(False)

    def set_value(self, value):
        if value is not None:
            self.native.setProgress(int(value))

    def rehint(self):
        # Android can crash when rendering some widgets until
        # they have their layout params set. Guard for that case.
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = at_least(self.native.getMeasuredHeight())
