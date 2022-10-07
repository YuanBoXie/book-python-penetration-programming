# 4-1 Socket
Socket 原义是“孔，插座”，通常我们翻译为套接字。

IP、TCP和HTTP分别位于网络层、传输层和应用层，但是Socket并不是TCP/IP协议族中的协议，而是一个**编程接口**。

TCP/IP是一个复杂的体系，类似Windows系统的Win32 API，Socket是TCP/IP对外提供的编程接口，通过Socket，可以不用自己去实现底层的三次握手等复杂细节，节省大量时间。

--------

TCP/IP是用于网络通信，因此Socket编程的主要目的是帮助网络上两个程序之间建立信息通道。socket又分为服务端socket和客户端socket，具体细节参考本目录下的代码实现。

```python
socket(family,type,[,protocal])
```
- family: AF_INET ==> IPv4  AF_INET6 ==> IPv6
- type: TCP类型 SOCK_STREAM UDP类型 SOCK_DGRAM 
```python
s = socket.socket() # ↓ equal to the following 默认值
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
- Note：原书本节示例代码在str和byte上存在一定问题，需要对类型进行转换。
- 关于send()、sendall()、sendto():
    send和sendall皆用于TCP发送数据，send不一定将内容全部发送，该函数返回成功发送的字节数，也就是说如果未全部成功发送，下次发送需要重传。sendall可以完整发送数据，如果未完整发送会报异常。sendto用于udp数据，不可靠传输。