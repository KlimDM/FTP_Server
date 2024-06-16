import threading
import os
import socket


class RequestHandler(threading.Thread):
    DIRECTORY = "./server_directory"

    def __init__(self, conn: socket):
        super().__init__()
        self.conn = conn
        os.chdir(self.DIRECTORY)

    def run(self):
        while True:
            self.handle_request()
        else:
            self.conn.close()

    def handle_request(self):
        data = self.conn.recv(1024).decode("utf-8")
        request = data.split(" ")
        command = request[0]
        print(f"Полученный запрос: '{command}'")
        try:
            if command == "pwd":
                self.conn.sendall(self.DIRECTORY.encode("utf-8"))
            elif command == "ls":
                self.conn.sendall("; ".join(os.listdir(os.getcwd())).encode("utf-8"))
            elif command == "mkdir":
                name = request[1]
                os.mkdir(name)
                self.conn.sendall(f"Папка {name} создана".encode("utf-8"))
            elif command == "rmdir":
                name = request[1]
                os.rmdir(name)
                self.conn.sendall(f"Папка {name} удалена".encode("utf-8"))
            elif command == "rmfile":
                name = request[1]
                os.remove(name)
                self.conn.sendall(f"Файл {name} удален".encode("utf-8"))
            elif command == "rename":
                prev_name = request[1]
                new_name = request[2]
                os.rename(prev_name, new_name)
                self.conn.sendall(f"Файл {prev_name} переименован в {new_name}".encode("utf-8"))
            elif command == "download":
                filename = request[1]
                self.download_file(filename)
            elif command == "upload":
                filename = request[1]
                self.upload_file(filename)
            else:
                self.conn.sendall(b"bad request")
        except Exception as e:
            self.conn.sendall(f"Ошибка: {e}".encode("utf-8"))

    def download_file(self, filename):
        filesize = os.path.getsize(filename)
        self.conn.send(f'file {filename} {filesize}'.encode("utf-8"))
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                self.conn.sendall(bytes_read)

    def upload_file(self, filename):
        with open(filename, 'wb') as f:
            while True:
                bytes_received = self.conn.recv(1024)
                f.write(bytes_received)
                break
        self.conn.sendall(f"file {filename} загружен на сервер".encode("utf-8"))