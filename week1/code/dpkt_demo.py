import dpkt
import datetime
pcap_path="Enter your path here"
f = open(pcap_path, 'rb')
pcap = dpkt.pcap.Reader(f)
for timestamp, data in pcap:
    ts=datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
    # print(ts, len(data))
    eth = dpkt.ethernet.Ethernet(data)
    # # do not proceed if there is no network layer data
    if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
        continue

    # # extract network layer data
    ip = eth.data

    # # do not proceed if there is no transport layer data
    if not isinstance(ip.data, dpkt.tcp.TCP):
        continue

    # # extract transport layer data
    tcp = ip.data

    # # do not proceed if there is no application layer data
    # # here we check length because we don't know protocol yet
    if not len(tcp.data) > 0:
        continue

    # # extract application layer data
    # ## if destination port is 80, it is a http request
    if tcp.dport == 80:
        try:
            http = dpkt.http.Request(tcp.data)
            print(http.headers)
        except:
            pass
            
    ## if source port is 80, it is a http response
    elif tcp.sport == 80:
        try:
            http = dpkt.http.Response(tcp.data)
            print(http.headers)
        except:
            pass