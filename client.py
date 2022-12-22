import socket 
import ssl 

context = ssl.create_default_context()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = context.wrap_socket(sock, server_hostname='127.0.0.1')
ssl_sock.connect(('127.0.0.1', 8443))
ssl_sock.send(b'Hello, world!')
data = ssl_sock.recv(1024)
print(data)
ssl_sock.close()
