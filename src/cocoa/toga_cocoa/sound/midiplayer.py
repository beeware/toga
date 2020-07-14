from toga_cocoa.libs import AVMIDIPlayer, NSURL


class MIDIPlayer:
    def __init__(self, interface, midi_sample, sound_font):
        self.interface = interface
        self.interface._impl = self
        self.native = None
        self.sound_font_url = None
        self.set_sample(midi_sample, sound_font)
        self.native.interface = self.interface

    def set_sample(self, midi_sample, sound_font=None):
        if isinstance(sound_font, NSURL):
            self.sound_font_url = sound_font
        elif sound_font:
            self.sound_font_url = NSURL.fileURLWithPath(str(sound_font))
        if self.native:
            self.native.autorelease()
        self.native = AVMIDIPlayer.alloc().initWithData(midi_sample, soundBankURL=self.sound_font_url, error=None)

    def play(self):
        callback = None
        self.native.play(callback)

    def stop(self):
        self.native.stop(None)

    def delete(self):
        self.native.release()

    def restart(self):
        self.native.currentPosition = 0
        self.play()

    @property
    def rate(self):
        return self.native.rate

    @rate.setter
    def rate(self, value):
        self.native.rate = value

    @property
    def current_time(self):
        return float(self.native.currentPosition)

    @current_time.setter
    def current_time(self, value):
        self.native.currentPosition = value

    @property
    def duration(self):
        return float(self.native.duration)

    @property
    def playing(self):
        return self.native.playing
