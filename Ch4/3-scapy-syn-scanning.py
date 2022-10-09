# 基于scapy进行SYN屏蔽扫描检查
from scapy.all import IP,TCP,sr,fuzz

ans, unans = sr(IP(dst="202.204.67.15")/fuzz(TCP(dport=80, flags="S")))

for s,r in ans:
    if r[TCP].flags == 18: # (SYN,ACK) 
        print("this port is open")
    if r[TCP].flags == 20: # (RST,ACK)
        print("this port is closed")
