import socket
 
host,port = '127.0.0.1',2345
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

response = client.recv(4096) #4k字节
client.close()
print("[*]recv resp:", response)