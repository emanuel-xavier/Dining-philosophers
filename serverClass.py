import time, socket, sys

class server():
    def __init__(self, port):
        self.s = socket.gethostname()
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.port = port
        
    def _bind (self):
        self.s.bind((self.host, self.port))

    def _listen (self, n):
        self.s.listen(n)

    def _accept (self):
        self.conn, self.addr = self.s.accept()
    
    def _send(self, msg):
        msg.encode()
        self.conn.send(msg)

    def _recv (self, size):
        msg = self.conn.recv(size)
        return msg.decode()

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

server = server(1234)
server._bind()
server._listen(1)
server._accept()

name = 'Server'

s_name = server._recv(1024)
print(s_name, "has connected to the chat room\nEnter [e] to exit chat room\n")
server._send(name.encode())

while True:
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        server._send(message.encode())
        print("\n")
        break
    server._send(message.encode())
    message = server._recv(1024)
    print(s_name, ":", message)