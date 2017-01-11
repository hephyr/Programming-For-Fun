#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scapy.all import *
global src_ip, dst_ip
src_ip = 1.1.1.1
dst_ip = 2.2.2.2
infile = "dump.pcap"

try:
    my_reader = PcapReader(infile)
    my_send(my_reader)
except IOError:
    print "Failed reading file %s contents" % infile
    sys.exit(1)


def my_send(rd, count=100):
    pkt_cnt = 0
    p_out = []

    for p in rd:
        pkt_cnt += 1
        np = p.payload
        np[IP].dst = dst_ip
        np[IP].src = src_ip
        del np[IP].chksum
        p_out.append(np)
        if pkt_cnt % count == 0:
            send(PacketList(p_out))
            p_out = []

    # Send remaining in final batch
    send(PacketList(p_out))
    print "Total packets sent %d" % pkt_cn
