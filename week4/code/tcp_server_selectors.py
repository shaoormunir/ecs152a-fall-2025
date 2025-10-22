import socket
import selectors

HOST = "127.0.0.1"
PORT = 65336

sel = selectors.DefaultSelector()


def accept(sock):
    client_socket, (client_host, client_port) = sock.accept()
    client_socket.setblocking(False)
    sel.register(client_socket, selectors.EVENT_READ, data=(client_host, client_port))


def service(client_socket, client_host, client_port):
    try:
        data = client_socket.recv(1024)
        if not data:
            print(f"Connection closed by {client_host}:{client_port}")
            sel.unregister(client_socket)
            client_socket.close()
            return
        print(f"Message from {client_host}:{client_port} - {data.decode()}")
        message = b"pong!"
        try:
            client_socket.sendall(message)
        except (BrokenPipeError, ConnectionResetError):
            print(f"Client {client_host}:{client_port} disconnected (broken pipe)")
            sel.unregister(client_socket)
            client_socket.close()
    except Exception as e:
        print(f"Error with client {client_host}:{client_port}: {e}")
        sel.unregister(client_socket)
        client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, data=None)

    while True:
        events = sel.select()
        for key, _ in events:
            if key.data is None:
                accept(key.fileobj)
            else:
                client_host, client_port = key.data
                service(key.fileobj, client_host, client_port)
