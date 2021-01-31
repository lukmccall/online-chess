import socket
import pickle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5555))

while True:
    data = pickle.loads(s.recv(1024 * 8))
    print(data)
    pass
