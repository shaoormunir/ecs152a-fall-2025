import random
import socket

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
PORT = 5001
SENDER_PORT = 5000

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    # bind the socket to a OS port
    udp_socket.bind(("localhost", PORT))

    # file to write to
    recv = open("recv.txt", "wb")

    # buffer to store the received data in
    message_buffer = b""

    # start receiving packets
    while True:
        timeouts = 0
        try:
            # receive the packet
            packet, _ = udp_socket.recvfrom(PACKET_SIZE)

            # get the message id
            seq_id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]

            # if the message id is -1, we have received all the packets
            seq_id = int.from_bytes(seq_id, signed=True, byteorder="big")
            print(f"Message with sequence id: {seq_id} received!")
            if seq_id == -1:
                break

            message_buffer += message

        except socket.timeout:
            timeouts += 1
            if timeouts > 3:
                break

    recv.seek(0)
    recv.write(message_buffer)
    recv.close()
