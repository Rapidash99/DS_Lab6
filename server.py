import socket
from threading import Thread
import os.path

clients = []


class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    def run(self):
        file_name = self.sock.recv(1024).decode()
        if os.path.isfile(file_name):
            for i in range(1000000000):
                index = file_name.rindex('.')
                if not os.path.isfile(file_name[:index] + '(Copy_' + str(i) + ')' + file_name[index:]):
                    file_name = file_name[:index] + '(Copy_' + str(i) + ')' + file_name[index:]
                    break

        file = open(file_name, 'wb')
        message = '{file_name} created'
        self.sock.send(message.encode())

        byte = self.sock.recv(1024)
        while byte:
            file.write(byte)
            byte = self.sock.recv(1024)
        self._close()

    def _broadcast(self, data):
        data = (self.name + '> ').encode() + data
        for u in clients:
            if u == self.sock:
                continue
            u.sendall(data)

    def _clear_echo(self, data):
        self.sock.sendall('\033[F\033[K'.encode())
        data = 'me> '.encode() + data
        self.sock.sendall(data)

    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')


if __name__ == "__main__":
    next_name = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen(10)
    while True:
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name = next_name + 1
        print(str(addr) + ' connected as ' + name)
        ClientListener(name, con).start()
