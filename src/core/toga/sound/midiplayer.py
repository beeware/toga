from toga.platform import get_platform_factory


class MIDIPlayer:
    """A player for MIDI file formats.  Although the data it plays is in the MIDI format, the MIDIPlayer itself is not a
    Musical Instrument Digital Interface (MIDI).

    Args:
        midi_sample (bytes): The MIDI sample to play.
        sound_font (str): The full path to the sound bank.  The sound bank must be a SoundFont2 (.sf2) bank.
    """

    def __init__(self, midi_sample, sound_font=None):
        self.factory = get_platform_factory()
        self._impl = self.factory.MIDIPlayer(interface=self, midi_sample=midi_sample, sound_font=sound_font)

    def set_sample(self, midi_sample, sound_font):
        self._impl.set_sample(midi_sample, sound_font)

    def play(self):
        self._impl.play()

    def stop(self):
        self._impl.stop()

    def delete(self):
        self._impl.delete()

    @property
    def rate(self):
        """
        Returns:
            The speed at which the sample is being played as a ``float``.  It acts as a multiplier on the tempo of the
            MIDI sample, with 1 being the default tempo, less than one slowing down playback, and greater than one
            speeding up playback.  It can be adjusted while playing.
        """
        return self._impl.rate

    @rate.setter
    def rate(self, value):
        if value == 0:
            raise ZeroDivisionError
        self._impl.rate = value

    @property
    def current_time(self):
        """
        Returns:
            The time in seconds that the playback is currently playing at as a ``float``.  Note that this is calculated
            assuming the original tempo, so dividing by the ``rate`` attribute gives the true playback time.  It can be
            (and is automatically) adjusted while playing.
        """
        return float(self._impl.current_time)

    @current_time.setter
    def current_time(self, value):
        self._impl.current_time = value

    @property
    def duration(self):
        """
        Returns:
            The duration of the playback in seconds as a ``float``.  Note that this is calculated assuming the original
            tempo, so dividing by the ``rate`` attribute gives the true duration.
        """
        return float(self._impl.duration)

    @property
    def playing(self):
        return self._impl.playing
