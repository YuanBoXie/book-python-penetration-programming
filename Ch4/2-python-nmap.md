# 4-2 python-nmap
网络扫描工具 Nmap 功能：
- (1)主机发现功能:向目标计算机发送信息，然后根据目标的反应来确定它是否处于开机并联网的状态。
- (2)端口扫描:向目标计机的指定端口发送信息，然后根据目标端口的反应判断它是否开放。
- (3)服务及版本检测:向目标计算机的目标端口发送特制的信息，然后根据目标的反应来检测它运行服务的服务类型和版本。
- (4)操作系统检测。

此外的高级功能：伪造发起扫描端的身份，进行隐蔽的扫描，规避目标的防御设备（例如防火墙），对系统进行安全漏洞检测，并提供完善的报告选项等。

-------------
python-nmap 作者博客：https://xael.org/

1.nmap下载地址： https://nmap.org/download.html
2.安装python-nmap模块：`pip install python-nmap`
python-nmap模块的核心就是PortScanner、PortScannerAsync、PortScannerError、PortScannerHostDict、PortScannrYield这5个类，其中最重要的是 PortScanner 类。PortScannerAsync是PortScanner的异步实现。

PortScanner
```
scan(self, hosts='l27.0.0.1', ports=None, arguments='-sV', sudo=False)
```
- hosts: 可以是ip或者域名
- ports: 支持单个端口（形如"80"）、多个端口（形如"80,443,8080"）、连续端口（形如"1-1000"）
- arguments: 参考nmap帮助文档
    - -sP 对目标进行 Ping 主机在线扫描
    - -sS 对目标进行一个TCP半开(SYN)类型端口扫描
    - -sT 对目标进行一个 TCP 全开类型的端口扫描
    - -sV 扫描目标网络服务软件版本
    - -PR 对目标进行一个 ARP 主机在线扫描
    - -O 扫描目标的操作系统类型

先用ifconfig查看网段，在测试具体的某个主机前需要通过nmap扫一下当前网段的所有主机：
```bash
nmap -sP 192.168.2.0/24
nmap -sP 10.116.0.0/16
```


PortScannerAsync
```
scan(self, hosts='l27.0.0.1', ports=None, arguments='-sV', callback=None, sudo=False)
```
- `callback(host,scan_data)`

PortScannerAsync 提供了三个实现异步的函数：
- still_scanning(): 如果扫描正在进行，则返回 True ，否则返回 False
- wait(self, timeout=None): 等待
- stop():停止扫描

