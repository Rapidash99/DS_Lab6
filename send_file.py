from socket import socket, AF_INET, SOCK_STREAM
from os.path import getsize
import sys


if __name__ == '__main__':
    if sys.argv[0] == 1:
        exit("You did not specified the file, address and port correctly")

    file_name = str(sys.argv[1])
    address = str(sys.argv[2])
    port = int(sys.argv[3])

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((address, port))

    sock.send(file_name.encode())

    size = getsize(file_name)
    file = open(file_name, "rb")
    byte = file.read(1024)
    bytes_sent = 0

    print(sock.recv(1024).decode())

    while byte:
        print("Transported " + str(bytes_sent * 100 // size) + "%")
        sock.send(byte)
        byte = file.read(1024)
        bytes_sent += 1024

    file.close()
    print("File transported")
    sock.close()
    print("Connection closed")
