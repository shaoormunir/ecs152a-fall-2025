import socket
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65336

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((SERVER_HOST, SERVER_PORT))
    try:
        while True:
            message = b"ping!"
            client.sendall(message)
            data = client.recv(1024)
            print(f"Message from server: {data.decode()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Client is shutting down.")
        client.close()
