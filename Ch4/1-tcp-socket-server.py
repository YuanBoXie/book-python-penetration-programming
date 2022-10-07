import socket

ip,port = '127.0.0.1', 2345

server = socket.socket()
server.bind((ip,port)) # server socket 绑定端口
server.listen(5) # 最大连接数

print("[*]Listening on %s:%d" % (ip,port))
while True:
    conn, addr = server.accept()
    print("[*]Accepted connection from: %s:%d" % (addr[0],addr[1]))
    
    conn.sendall(bytes("hello,world!", encoding="utf-8"))
    conn.close()