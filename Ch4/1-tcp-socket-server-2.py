"""
增加了threading线程处理的写法
"""
import socket
import threading

ip,port = '127.0.0.1', 2345

server = socket.socket()
server.bind((ip,port)) # server socket 绑定端口
server.listen(5) # 最大连接数

def handle_client(client_socket):
    request = client_socket.recv(1024)#1k
    print("[*]Received: %s" % request)
    client_socket.send("ACK!")
    client_socket.close()

print("[*]Listening on %s:%d" % (ip,port))
while True:
    conn, addr = server.accept()
    print("[*]Accepted connection from: %s:%d" % (addr[0],addr[1]))

    #挂起线程处理传入的数据
    client_handler = threading.Thread(target=handle_client,args = (conn,))
    client_handler.start()