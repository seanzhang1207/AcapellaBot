import serial
import time
from aupyom import Sound

from RealSenseJSONServer import RealSenseJSONServer
from SpeechUdpServer import SpeechUdpServer
from BleUdpServer import BleUdpServer
from VariableSpeedWavePlayer import VariableSpeedWavePlayer

#board_serial = serial.Serial(write_timeout=0.5)
#board_serial.baudrate = 115200
#board_serial.port = "COM4"

speech_paths = [
    'changdehao.wav',
    'haobangya.wav',
    'kaixinzaijian.wav',
    'lingerxiangdingdang.wav',
    'nanihuichangshenmege.wav',
    'nihaoya.wav',
    'paishouge.wav',
    'xiexiepeihe.wav',
    'yiqichang.wav',
    'yiqichangba.wav',
    'zhihuibang.wav'
]

speech_prefix = "interaction/"

song_paths = [
    'bell.wav',
    'slap.wav',
    'star.wav'
]

song_prefix = "music/"

STATE = "find_face"
FACE = False
BPM = 60
SONG = None
ANSWER = None
FACEX = 100


def face_callback(face):
    global STATE, FACE, BPM, SONG, ANSWER, FACEX
    face_x = face["box_x"] + face["box_w"] / 2 - 330
    FACEX = face_x
    print(str(face_x))
    if abs(face_x) > 20 :
        pass
    else:
        FACE = True


def speech_callback(id):
    global STATE, FACE, BPM, SONG, ANSWER, FACEX
    if id <= 20:
        #YES
        ANSWER = 'YES'
    else:
        #NO
        ANSWER = 'NO'

def ble_callback(bpm):
    global STATE, FACE, BPM, SONG, ANSWER, FACEX
    BPM = bpm


speeches = {}
for speech in speech_paths:
    speeches[speech] = Sound.from_file(speech_prefix + speech)

songs = {}
for song in song_paths:
    songs[song] = Sound.from_file(song_prefix + song)


print(speeches)

print(songs)

faceserver = RealSenseJSONServer(callback=face_callback)
speechserver = SpeechUdpServer(callback=speech_callback)
beatserver = BleUdpServer(callback=ble_callback)
player = VariableSpeedWavePlayer()

#board_serial.open()

faceserver.start()
speechserver.start()
beatserver.start()

while True:

    STATE = "find_face"
    FACE = False
    BPM = 60
    SONG = None
    ANSWER = None
    FACEX = 100

    print('=== ' + STATE + ' ===')

    while abs(FACEX) > 20 :
        print("searching... " + str(abs(FACEX)))
        try:
            if FACEX < 0:
                board_serial.write(b'l')
            elif FACEX > 0:
                board_serial.write(b'r')
        except:
            print("timeout")
        time.sleep(0.1)

    try:
        board_serial.write(b's')
    except:
        print("timeout")

    STATE = "interaction"

    print('=== ' + STATE + ' ===')

    player.load_audio(speeches['nihaoya.wav'])
    player.play_block()

    while not ANSWER:
        time.sleep(0.5)

    if ANSWER == "NO":
        ANSWER = None

        time.sleep(0.5)
        player.load_audio(speeches['lingerxiangdingdang.wav'])
        player.play_block()

        while not ANSWER:
            time.sleep(0.5)

        if ANSWER == "NO":
            ANSWER = None

            time.sleep(0.5)
            player.load_audio(speeches['paishouge.wav'])
            player.play_block()

            while not ANSWER:
                time.sleep(0.5)

            if ANSWER == "NO":
                ANSWER = None

                time.sleep(0.5)
                player.load_audio(speeches['nanihuichangshenmege.wav'])
                player.play_block()
                pass
            else:
                #slap.wav
                player.load_audio(speeches['yiqichangba.wav'])
                player.play_block()
                time.sleep(0.5)
                player.load_audio(speeches['zhihuibang.wav'])
                player.play_block()
                time.sleep(0.5)

                player.load_audio(songs['slap.wav'])
                player.play()
                while player.playing():
                    player.set_speed(BPM / 60)
                    time.sleep(0.1)
        else:
            #bell.wav
            player.load_audio(speeches['yiqichang.wav'])
            player.play_block()
            time.sleep(0.5)
            player.load_audio(speeches['zhihuibang.wav'])
            player.play_block()
            time.sleep(0.5)

            player.load_audio(songs['bell.wav'])
            player.play()
            while player.playing():
                player.set_speed(BPM / 60)
                time.sleep(0.1)
    else:
        #star.wav
        player.load_audio(speeches['yiqichangba.wav'])
        player.play_block()
        time.sleep(0.5)
        player.load_audio(speeches['zhihuibang.wav'])
        player.play_block()
        time.sleep(0.5)

        player.load_audio(songs['star.wav'])
        player.play()
        while player.playing():
            player.set_speed(BPM / 60)
            time.sleep(0.1)

    STATE = "done_interaction"

    print('=== ' + STATE + ' ===')

    time.sleep(0.5)
    player.load_audio(speeches['changdehao.wav'])
    player.play_block()
    time.sleep(0.5)
    player.load_audio(speeches['kaixinzaijian.wav'])
    player.play_block()







