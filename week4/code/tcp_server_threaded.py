import socket
import threading

HOST = "127.0.0.1"
PORT = 65336


def handle_client(client_socket, client_host, client_port):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection closed by {client_host}:{client_port}")
                break
            print(f"Message from {client_host}:{client_port} - {data.decode()}")
            message = b"pong!"
            try:
                client_socket.sendall(message)
            except (BrokenPipeError, ConnectionResetError):
                print(f"Client {client_host}:{client_port} disconnected (broken pipe)")
                break
    except Exception as e:
        print(f"Error with client {client_host}:{client_port}: {e}")
    finally:
        client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    while True:
        client_socket, (client_host, client_port) = server.accept()
        threading.Thread(
            target=handle_client,
            args=(client_socket, client_host, client_port),
            daemon=True,
        ).start()
