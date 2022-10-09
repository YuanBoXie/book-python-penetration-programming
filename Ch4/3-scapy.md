# 4-3 Scapy
- 区分scapy和scrapy：
  scapy是一个操作网络数据包的工具(Packet crafting),scrapy是一个爬虫框架。

scapy 文档地址：https://www.osgeo.cn/scapy/introduction.html
```bash
pip install scapy
```
Scapy 是一个 Python 程序，它允许用户发送、嗅探、分析和伪造网络包。这种能力允许构建能够探测、扫描或攻击网络的工具。scapy 在内部实现了大量的网络协议(DNS\ARP\IP\TCP\UDP等),可以用它来编写对网络数据包的发送、监昕和解析。该模块比 nmap 更底层，可以更为直观了解到网络中的各种扫描和攻击行为。在 Scapy 中，每一个协议就是一个类，需要实例化一个协议类，就可以创建一个该协议的数据包。

Scapy 提供了和 Python 样的交互式命令行。这里需要特别强调的是，虽然本书中 Scapy 作为 Python 一个模块存在，但是 Scapy 本身就是一个可以运行的工具， 它自己具备一个独立的运行环境，因而可以不在 Python 环境下运行。

- 命令行输入scapy进入其命令行环境。在该环境中可以进行如下示例操作：（注意：不是python交互式环境）
```bash
构造单个数据包
>>> ip = IP(dst="202.204.67.15")
>>> ip
<IP  dst=202.204.67.15 |>
批量数据包
>>> target = "10.116.0.0/16"
>>> ip = IP(dst=target)
>>> ip
<IP  dst=Net("10.116.0.0/16") |>
>>> 
查看数据包
>>> [p for p in ip]
[<IP  dst=10.116.0.0 |>, 
 <IP  dst=10.116.0.1 |>, 
 <IP  dst=10.116.0.2 |>, 
 <IP  dst=10.116.0.3 |>, 
 <IP  dst=10.116.0.4 |>, 
 ...]
```
- Scapy 采用分层的形式来构造数据包，通常最下面的一个协议为 Ether，然后是 IP，再之后是 TCP 或者是 UDP。
- **Note**:ARP协议无法用IP()构造，因此只能用Ether()。Ether()可以设置发送方和接收方的 MAC 地址。
```bash
构造广播数据包
>>> Ether(dst="ff:ff:ff:ff:ff:ff")
<Ether  dst=ff:ff:ff:ff:ff:ff |>
```
- scapy分层符号通过`/`实现，一个数据包是由多层协议组合而成，那么协议之间可以通过“/”分割开，按照协议自底向上从左向右排列。
```bash
>>> Ether()/IP()/TCP()
<Ether  type=IPv4 |<IP  frag=0 proto=tcp |<TCP  |>>>
```

- Ether类:源地址、目的地址和类型
- IP类:源地址,目的地址,版本,长度,协议类型,校验和等，
- TCP类:源端口号,目的端口号

查看一个类的属性
```bash
>>> ls(Ether())
dst        : DestMACField                        = WARNING: Mac address to reach destination not found. Using broadcast.
'ff:ff:ff:ff:ff:ff' ('None')
src        : SourceMACField                      = '34:c9:3d:e7:02:d9' ('None')
type       : XShortEnumField                     = 36864           ('36864')
>>> ls(IP())
version    : BitField  (4 bits)                  = 4               ('4')
ihl        : BitField  (4 bits)                  = None            ('None')       
tos        : XByteField                          = 0               ('0')
len        : ShortField                          = None            ('None')       
id         : ShortField                          = 1               ('1')
flags      : FlagsField                          = <Flag 0 ()>     ('<Flag 0 ()>')
frag       : BitField  (13 bits)                 = 0               ('0')
ttl        : ByteField                           = 64              ('64')
proto      : ByteEnumField                       = 0               ('0')
chksum     : XShortField                         = None            ('None')
src        : SourceIPField                       = '127.0.0.1'     ('None')
dst        : DestIPField                         = '127.0.0.1'     ('None')
options    : PacketListField                     = []              ('[]')
```

发送数据包：send()\sendp()
区别：send()工作在第三层(网络层,IP数据包)，sendp()工作在第二层(链路层,Ether数据包)。

ICMP包
```bash
>>> send(IP(dst="202.204.67.15")/ICMP())
.
Sent 1 packets.
```
以太网广播
```bash
>>> sendp(Ether(dst="ff:ff:ff:ff:ff:ff"))
.
Sent 1 packets.
```
注意: 这两个函数只发不收。

如果希望发送一个内容是随机填充的数据包，而且又要保证这个数据包的正确性，那么用fuzz()函数:
```bash
>>> IP(dst="202.204.67.15"/fuzz(TCP()))
<IP  dst=<Raw  load='202.204.67.15' |<TCP  |>> |>
```

如果需要接收数据包：sr(),sr1(),srp()
sr()、sr1()用于第三层（IP/ARP/..),srp()用于第二层。
```bash
>>> sr(IP(dst="202.204.67.15")/ICMP())
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
(<Results: TCP:0 UDP:0 ICMP:1 Other:0>,
 <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>)

>>> ans,unanser = sr(IP(dst="202.204.67.15")/ICMP())
Begin emission:
Finished sending 1 packets.
...*
Received 4 packets, got 1 answers, remaining 0 packets
>>> ans
<Results: TCP:0 UDP:0 ICMP:1 Other:0>
>>> unanser
<Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>
>>> 
```
sr1()就是sr只返回第一个应答的包
```bash
>>> sr1(IP(dst="202.204.67.15")/ICMP())
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
<IP  version=4 ihl=5 tos=0x0 len=28 id=1457 flags= frag=0 ttl=62 proto=icmp chksum=0xf4ea src=202.204.67.15 dst=10.116.105.246 |<ICMP  type=echo-reply code=0 chksum=0xffff id=0x0 seq=0x0 |<Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |>>>
```
可以利用 sr1() 函数来测试目标的某个端口是否开放，采用半开扫描(SYN)的办法
```bash
>>> sr1(IP(dst="202.204.67.15")/TCP(dport=80,flags="S"))
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
<IP  version=4 ihl=5 tos=0x0 len=44 id=0 flags=DF frag=0 ttl=62 proto=tcp chksum=0xba86 src=202.204.67.15 dst=10.116.105.246 |<TCP  sport=http dport=ftp_data seq=1026221283 ack=1 dataofs=6 reserved=0 flags=SA window=14600 chksum=0xba9f urgptr=0 options=[('MSS', 1386)] |<Padding  load='\x00\x00' |>>>
```
scapy命令行中使用sniff()开始监听，但不会立即显示数据包，ctrl+c暂停监听后才显示。
```bash
>>> sniff()
<Sniffed: TCP:4 UDP:0 ICMP:0 Other:0>
>>> sniff(filter="icmp")
>>> sniff(filter="host 202.204.67.15")
<Sniffed: TCP:25 UDP:0 ICMP:0 Other:0>
>>> sniff(filter="host 202.204.67.15 and icmp") # 组合条件
>>> sniff(iface="eth1") # 指定网卡
>>> sniff(count=3)  # 计数，满足后结束
```
如果要查看sniff的数据结果，使用`_`,`_`表示上一条语句执行结果。
```bash
>>> a = _
>>> a
<Sniffed: TCP:25 UDP:0 ICMP:0 Other:0>
>>> a.nsummary() # 显示数据包
0000 Ether / IP / TCP 10.116.105.246:17630 > 202.204.67.15:http S 
0001 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17630 SA
0002 Ether / IP / TCP 10.116.105.246:17630 > 202.204.67.15:http A 
0003 Ether / IP / TCP 10.116.105.246:17630 > 202.204.67.15:http PA / Raw
0004 Ether / IP / TCP 10.116.105.246:17630 > 202.204.67.15:http PA / Raw
0005 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17630 A / Padding
0006 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17630 A / Padding
0007 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17630 PA / Raw
0008 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17630 FA / Padding
0009 Ether / IP / TCP 10.116.105.246:17630 > 202.204.67.15:http A
0010 Ether / IP / TCP 10.116.105.246:17630 > 202.204.67.15:http FA
0011 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17630 A / Padding
0012 Ether / IP / TCP 10.116.105.246:17633 > 202.204.67.15:http S
0013 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 SA
0014 Ether / IP / TCP 10.116.105.246:17633 > 202.204.67.15:http A
0015 Ether / IP / TCP 10.116.105.246:17633 > 202.204.67.15:http PA / Raw
0016 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 A / Padding
0017 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 A / Raw
0018 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 A / Raw
0019 Ether / IP / TCP 10.116.105.246:17633 > 202.204.67.15:http A
0020 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 PA / Raw
0021 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 FA / Padding
0022 Ether / IP / TCP 10.116.105.246:17633 > 202.204.67.15:http A
0023 Ether / IP / TCP 10.116.105.246:17633 > 202.204.67.15:http FA
0024 Ether / IP / TCP 202.204.67.15:http > 10.116.105.246:17633 A / Padding
```
pkt.summary() 摘要显示pkt内容 
```bash
>>> p = IP(dst="www.baidu.com")
>>> p.summary()
'10.116.105.246 > Net("www.baidu.com/32") ip'
```

## 基于 Scapy 实现 ACK 类型的端口扫描
描述：对某IP进行ACK类型的扫描，判断21、23、135、443、445端口是否被屏蔽（屏蔽不等于关闭)。
根据TCP三次握手规则，对一个open的端口发ack包会回复ack，关闭的端口回复rst。如果未回复，说明被屏蔽。
```bash
>>> ans,unans = sr(IP(dst="202.204.67.15")/TCP(dport=[21,23,135,443,445],flags="A"))
Begin emission:
Finished sending 5 packets.
.....*.**.*...............................................................
Received 74 packets, got 4 answers, remaining 1 packets
(<Results: TCP:4 UDP:0 ICMP:0 Other:0>,
 <Unanswered: TCP:1 UDP:0 ICMP:0 Other:0>)

查看未过滤端口
>>> for s,r in ans:
...:   if s[TCP].dport == r[TCP].sport:
...:     print(str(s[TCP].dport)+" is unfiltered")
...: 
23 is unfiltered
135 is unfiltered
443 is unfiltered
445 is unfiltered
查看被过滤端口
>>> for s in unans:
...:     print(str(s[TCP].dport)+ " is filtered")
...: 
21 is filtered
```
