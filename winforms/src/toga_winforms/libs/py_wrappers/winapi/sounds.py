from __future__ import annotations

import ctypes

MB_ICONASTERISK = 0x40

def play_system_sound(sound_type):
    ctypes.windll.user32.MessageBeep(sound_type)


if __name__ == "__main__":
    play_system_sound(0x40)  # MB_ICONASTERISK