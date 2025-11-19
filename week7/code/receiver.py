import socket
import random

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
PORT = 5001
SENDER_PORT = 5000


def create_ack(seq_id):
    return int.to_bytes(seq_id, SEQ_ID_SIZE, byteorder="big", signed=True) + b"ack"


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

            if random.random() < 0.2:
                print(f"Packet with seq id {seq_id} dropped.")
                continue

            ack_message = create_ack(seq_id)
            udp_socket.sendto(ack_message, ("localhost", SENDER_PORT))

            message_buffer += message

        except socket.timeout:
            timeouts += 1
            if timeouts > 3:
                break

    recv.seek(0)
    recv.write(message_buffer)
    recv.close()
