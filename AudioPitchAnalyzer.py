import pyaudio
from threading import Thread
import numpy as np
import aubio


class AubioThread (Thread):

    stop = False

    def __init__(self):
        Thread.__init__(self)
        # initialise pyaudio
        self.p = pyaudio.PyAudio()

        # open stream
        self.buffer_size = 1024
        pyaudio_format = pyaudio.paFloat32
        n_channels = 1
        samplerate = 44100
        self.stream = self.p.open(format=pyaudio_format,
                        channels=n_channels,
                        rate=samplerate,
                        input=True,
                        frames_per_buffer=self.buffer_size)

        # setup pitch
        tolerance = 0.8
        win_s = 4096  # fft size
        hop_s = self.buffer_size  # hop size
        self.pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
        self.pitch_o.set_unit("midi")
        self.pitch_o.set_tolerance(tolerance)
        self.pitch = 0
        self.confidence = 0
        self.current_pitch = 0
        self.notes = []

    def run(self):
        print("* pitch analyzer started")

        while self.current_pitch == 0:
            audiobuffer = self.stream.read(self.buffer_size)
            signal = np.fromstring(audiobuffer, dtype=np.float32)

            self.pitch = self.pitch_o(signal)[0]
            self.confidence = self.pitch_o.get_confidence()

            if self.confidence > 0.8:
                self.current_pitch = self.pitch
                break

        while not self.stop:
            audiobuffer = self.stream.read(self.buffer_size)
            signal = np.fromstring(audiobuffer, dtype=np.float32)

            self.pitch = self.pitch_o(signal)[0]
            self.confidence = self.pitch_o.get_confidence()
            if self.confidence > 0.9:
                if abs(self.current_pitch - self.pitch) > 0.9 and self.pitch > 0:
                    #print("{} / {}".format(self.pitch, self.confidence))
                    #print(abs(self.current_pitch - self.pitch))
                    print(self.pitch)
                    self.current_pitch = self.pitch
                    self.notes.append(self.pitch)





        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("* pitch analyzer stopped")


class AudioPitchAnalyzer:

    aubio = None
    started = False

    def __init__(self):
        pass

    def start(self):
        self.aubio = AubioThread()
        self.aubio.start()
        self.started = True

    def stop(self):
        if self.started:
            self.aubio.stop = True
        while self.aubio.is_alive():
            pass

    def is_recording(self):
        return self.aubio.is_alive()

    def get_pitch(self):
        return self.aubio.pitch

    def get_confidence(self):
        return self.aubio.confidence


analyzer = AudioPitchAnalyzer()
analyzer.start()
while True:
    a = input()
    print(a)
    analyzer.stop()
    print(analyzer.aubio.notes)
    break
