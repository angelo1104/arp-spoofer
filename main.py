import scapy.all as scapy

packet = scapy.ARP(op=2, pdst='192.168.43.1', hwdst='ac:c3:3a:66:96:34', psrc='192.168.43.1')

print(packet.summary())
