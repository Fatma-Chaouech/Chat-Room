import ssl
import socket

#Create an SSL context: An SSL context holds the necessary configuration and certificates for establishing an SSL/TLS connection. To create an SSL context, you can use the create_default_context function from the ssl module.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('example.com', 8443))
sock.listen()


# The difference between sock.connect and sock.bind
# connect is in the client code

# When do we wrap sockets?
