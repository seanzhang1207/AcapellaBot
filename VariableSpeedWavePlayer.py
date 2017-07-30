from aupyom import Sampler, Sound
import time


class VariableSpeedWavePlayer:

    sampler = None
    audio = None

    def __init__(self):
        self.sampler = Sampler()

    def load_audio(self, audio):
        self.audio = audio

    def load_chunk(self, chunk, sr=22050):
        self.audio = Sound(chunk, sr=sr)

    def play(self):
        if self.audio:
            self.sampler.play(self.audio)

    def play_block(self):
        if self.audio:
            self.sampler.play(self.audio)
            while self.audio.playing:
                time.sleep(0.1)

    def set_speed(self, speed):
        self.audio.stretch_factor = speed

    def set_pitch(self, pitch):
        self.audio.pitch_shift = pitch

    def playing(self):
        return self.audio.playing

    def stop(self):
        self.audio.playing = False

