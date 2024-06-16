import os
import socket

HOST = 'localhost'
PORT = 6666
DIRECTORY = "./client_directory"

os.chdir(DIRECTORY)
sock = socket.socket()
sock.connect((HOST, PORT))

while True:
    request = input('Введите команду > ')
    if request.startswith("quit"):
        break
    elif request.startswith("download"):
        filename = request.split(' ')[1]
        sock.send(request.encode())
        response = sock.recv(1024).decode("utf-8")
        if response.startswith('file'):
            _, filename, filesize = response.split(' ')
            filesize = int(filesize)
            received_size = 0
            with open(filename, 'wb') as f:
                while received_size < filesize:
                    bytes_received = sock.recv(1024)
                    if not bytes_received:
                        break
                    f.write(bytes_received)
                    received_size += len(bytes_received)
            print(f"Файл {filename} успешно загружен с сервера.")
    elif request.startswith("upload"):
        sock.send(request.encode("utf-8"))
        filename = request.split(' ')[1]
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                sock.sendall(bytes_read)
        print(sock.recv(1024).decode("utf-8"))
    else:
        sock.send(request.encode())
        response = sock.recv(1024).decode("utf-8")
        print(response)