from .main_window_proxy import MainWindowProxy

class AppProxy:
    """Minimal app proxy: only expose main_window."""
    @property
    def main_window(self):
        return MainWindowProxy()