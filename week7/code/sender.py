import socket
import argparse

# total packet size
PACKET_SIZE = 1024
# bytes reserved for sequence id
SEQ_ID_SIZE = 4
# bytes available for message
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
# total packets to send
WINDOW_SIZE = 20
# PORT of sender
PORT = 5000
# PORT of receiver
PORT_RECV = 5001

parser = argparse.ArgumentParser("Send files the receiver running on the localhost")

parser.add_argument("--input_file", type=str, default="send.txt", required=False)

args = parser.parse_args()

input_file = args.input_file

# read data
with open(input_file, "rb") as f:
    data = f.read()

# create a udp socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

    # bind the socket to a OS port
    udp_socket.bind(("localhost", PORT))
    udp_socket.settimeout(1)

    # start sending data from 0th sequence
    seq_id = 0
    while seq_id < len(data):

        # create messages
        messages = []
        seq_id
        for i in range(WINDOW_SIZE):
            # construct messages
            # sequence id of length SEQ_ID_SIZE + message of remaining PACKET_SIZE - SEQ_ID_SIZE bytes
            message = (
                int.to_bytes(seq_id, SEQ_ID_SIZE, byteorder="big", signed=True)
                + data[seq_id : seq_id + MESSAGE_SIZE]
            )
            messages.append((seq_id, message))
            # move seq_id tmp pointer ahead
            seq_id += MESSAGE_SIZE

        # send messages
        for _, message in messages:
            udp_socket.sendto(message, ("localhost", PORT_RECV))

    # send final closing message
    udp_socket.sendto(
        int.to_bytes(-1, 4, signed=True, byteorder="big"), ("localhost", PORT_RECV)
    )()
