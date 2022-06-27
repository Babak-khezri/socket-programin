import socket
import threading
import os

IP = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
SIZE = 1024


def main():
    
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen()
        print("[STARTING] Server is starting...")
        connection, address = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(connection, address))
        thread.start()


def handle_client(conn, addr):

    print(f"[NEW CONNECTION] {addr} conected.")

    connected = True

    while connected:
        try:
            request_header = conn.recv(SIZE).decode(FORMAT)
            if request_header == 'ls':
                list_of_files = "  ".join(os.listdir())
                conn.send(list_of_files.encode(FORMAT))
            elif request_header == 'put':
                filename = conn.recv(SIZE).decode(FORMAT)
                file = open(filename, "w")
                conn.send("file recived".encode(FORMAT))
                data = conn.recv(SIZE).decode(FORMAT)
                file.write(data)
                file.close()
            elif request_header == 'get':
                filename = conn.recv(SIZE).decode(FORMAT)
                try:
                    file = open(filename, 'r')
                    data = file.read()
                    file.close()
                    conn.send("File is downloading...".encode(FORMAT))
                    conn.send(data.encode(FORMAT))

                except Exception:
                    conn.send("File not found!".encode(FORMAT))
        except Exception:
            print(f"[CONNECTION] {addr} disconected.")
            connected = False

    conn.close()


if __name__ == '__main__':
    main()
