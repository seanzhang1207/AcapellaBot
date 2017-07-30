from VariableSpeedWavePlayer import VariableSpeedWavePlayer
from AudioPitchAnalyzer import AudioPitchAnalyzer
from BleUdpServer import BleUdpServer

import random
import time
from aupyom import Sampler, Sound

from threading import Thread

import pygame
import pygame.midi


class GeneratorThread (Thread):
    stop = False

    def __init__(self):
        Thread.__init__(self)
        self.bpm = 150

        #self.player = VariableSpeedWavePlayer()
        self.analyzer = AudioPitchAnalyzer()
        self.beat = 0

        self.beats = []
        #self.sampler = Sampler()

        #for fname in ALL:
        #    print(fname)
        #    self.beats.append(Sound.from_file("voices/" + fname))


        self.analyzer.start()

        pygame.midi.init()
        self.player = pygame.midi.Output(pygame.midi.get_default_output_id())
        self.player.set_instrument(50, 1)

    def run(self):
        last_shift = 0
        while not self.stop:

            print(self.bpm)

            if self.analyzer.get_confidence() > 0.9:
                pitch_shift = int(self.analyzer.get_pitch()) - 63
                last_shift = pitch_shift
            else:
                pitch_shift = last_shift

            note = int(self.analyzer.get_pitch())

            if self.beat == 0:
                self.player.note_on(note, 127, 1)
                time.sleep(60 / self.bpm)
                self.player.note_off(note, 127, 1)
            elif self.beat == 1:
                self.player.note_on(note+4, 127, 1)
                time.sleep(60 / self.bpm)
                self.player.note_off(note+4, 127, 1)
            elif self.beat == 2:
                self.player.note_on(note+7, 127, 1)
                time.sleep(60 / self.bpm)
                self.player.note_off(note+7, 127, 1)
            elif self.beat == 3:
                self.player.note_on(note+4, 127, 1)
                time.sleep(60 / self.bpm)
                self.player.note_off(note+4, 127, 1)

            self.beat = (self.beat + 1)%4


ALL = [
    'a1.wav',
    #'a2.wav',
    'aa1.wav',
    #'aa2.wav',
    'ba1.wav',
    #'ba2.wav',
    'baba1.wav',
    #'baba2.wav',
    #'ci.wav',
    #'cici.wav',
    'da1.wav',
    #'da2.wav',
    'dada1.wav',
    #'dada2.wav',
    'dong1.wav',
    #'dong2.wav',
    'dongdong1.wav',
    #'dongdong2.wav',
    'en1.wav',
    #'en2.wav',
    'la1.wav',
    #'la2.wav',
    'lala1.wav',
    #'lala2.wav',
    'na1.wav',
    #'na2.wav',
    'nana1.wav',
    #'nana2.wav',
    'wa1.wav',
    #'wa2.wav',
    'wawa1.wav',
    #'wawa2.wav',
    'u1.wav',
    #'u2.wav'
]

STRONG_SINGLE = [
    'ba1.wav', 'ba2.wav', 'da1.wav', 'da2.wav', 'dong1.wav', 'dong2.wav'
]

STRONG_DOUBLE = [
    'baba1.wav', 'baba2.wav', 'dada1.wav', 'dada2.wav', 'dongdong1.wav', 'dongdong2.wav'
]

WEAK_SINGLE = [
    'ba1.wav', 'ba2.wav', 'ci.wav', 'da1.wav', 'da2.wav', 'la1.wav',
    'la2.wav', 'na1.wav', 'na2.wav', 'wa1.wav', 'wa2.wav', 'u1.wav',
    'u2.wav'
]

WEAK_DOUBLE = [
    'baba1.wav', 'baba2.wav', 'cici.wav', 'dada1.wav', 'dada2.wav', 'lala1.wav', 'lala2.wav', 'nana1.wav',
    'nana2.wav', 'wawa1.wav', 'wawa2.wav'
]

MEDIUM = [
    'aa1.wav', 'aa2.wav', 'en1.wav', 'en2.wav', 'wu1.wav', 'wu2.wav'
]

LONG = [
    'wu1.wav', 'wu2.wav'
]

SPEECH = {

}


class AcapellaGenerator:

    def __init__(self):
        self.beatserver = BleUdpServer(callback=self.generate)
        self.beatserver.start()
        self.generator = GeneratorThread()
        self.generator.start()

    def generate(self, data):
        self.generator.bpm = ord(data)

generator = AcapellaGenerator()

while True:
    time.sleep(0.1)