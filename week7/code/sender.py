import socket
import argparse
import time

# total packet size
PACKET_SIZE = 1024
# bytes reserved for sequence id
SEQ_ID_SIZE = 4
# bytes available for message
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
# total packets to send
WINDOW_SIZE = 40
# PORT of sender
PORT = 5000
# PORT of receiver
PORT_RECV = 5001

parser = argparse.ArgumentParser("Send files to the receiver running on the localhost")

parser.add_argument("--input_file", type=str, default="send.txt", required=False)

args = parser.parse_args()

input_file = args.input_file

# read data
with open(input_file, "rb") as f:
    data = f.read()

start_time = time.time()

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
        acks = {}
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
            acks[seq_id] = False

        # send messages
        for id, message in messages:
            udp_socket.sendto(message, ("localhost", PORT_RECV))

        while True:
            try:
                packet, _ = udp_socket.recvfrom(PACKET_SIZE)
                seq_id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]

                seq_id = int.from_bytes(seq_id, signed=True, byteorder="big")

                print(f"Acknowledgement for seq id: {seq_id} received.")
                acks[seq_id] = True
                if all(acks.values()):
                    break
            except TimeoutError:
                print(f"Packet with seq id {id} timed out.")
                for failed_seq_ids in [sid for sid in acks.keys() if not acks[sid]]:
                    udp_socket.sendto(
                        (
                            int.to_bytes(
                                failed_seq_ids,
                                SEQ_ID_SIZE,
                                byteorder="big",
                                signed=True,
                            )
                            + data[failed_seq_ids : failed_seq_ids + MESSAGE_SIZE]
                        ),
                        ("localhost", PORT_RECV),
                    )

    # send final closing message
    udp_socket.sendto(
        int.to_bytes(-1, 4, signed=True, byteorder="big"), ("localhost", PORT_RECV)
    )
    end_time = time.time()
    throughput = len(data) / (end_time - start_time)
    print(f"The througput of the program is: {throughput}")
