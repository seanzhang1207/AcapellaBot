from threading import Thread
import socket
import json


class RealSenseJSONServer (Thread):

    stop = False

    def __init__(self, ip="0.0.0.0", port=34820, callback=None):
        Thread.__init__(self)
        self.IP = ip
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.IP, self.PORT))
        self.callback = callback

    def run(self):
        while not self.stop:
            data, addr = self.socket.recvfrom(1024)
            if self.callback:
                self.callback(json.loads(data))

        self.socket.close()

