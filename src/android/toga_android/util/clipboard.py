from ..libs import android


class Clipboard():
    clipboard_manager = None

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._native_activity = MainActivity.singletonThis
        self.clipboard_manager = self._native_activity.getSystemService(self._native_activity.CLIPBOARD_SERVICE)

    def get_text(self):
        if self.clipboard_manager.hasPrimaryClip():
            clip_data = self.clipboard_manager.getPrimaryClip()
            item = clip_data.getItemAt(0)
            if item.getText() is not None:
                return item.getText().toString()
            else:
              return None
        else:
            return None

    def set_text(self, text):
        if text is None:
            self.clipboard_manager.clearPrimaryClip()
        else:
            clip_data = ClipData.newPlainText("Text", text);
            self.clipboard_manager.setPrimaryClip(clip_data);

