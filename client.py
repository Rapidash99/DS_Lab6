from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import sys


class Client(Thread):
    def __init__(self):
        super().__init__(daemon=True)

    def run(self):


if __name__ == '__main__':
    if sys.argv[0] == 1:
        exit("You did not specified the file, address and port correctly")

    file = sys.argv[1]
    address = sys.argv[2]
    port = int(sys.argv[3])

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.connect((address, port))

