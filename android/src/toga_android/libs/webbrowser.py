import webbrowser

from android.content import Intent
from android.net import Uri
from org.beeware.android import MainActivity


class AndroidBrowser:
    def open(self, url, new=0, autoraise=True):  # pragma: no cover
        # Create the Intent to view the URL
        intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))

        # Android requires the 'New Task' flag if launching from a non-Activity context.
        # Since we are launching from the main activity context, we probably don't need
        # it, but it doesn't hurt to include it to be safe.
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

        # Launch the intent
        MainActivity.singletonThis.startActivity(intent)
        return True


def register_webbrowser():
    webbrowser.register(
        "android",
        None,
        AndroidBrowser(),
        preferred=True,
    )
