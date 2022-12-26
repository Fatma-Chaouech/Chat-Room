# Import the necessary classes and functions
from src.openssl_client import OpenSSLClient
from src.room import Room
from src.ldap_client import LDAPClient
from src.user import User
from src.message import Message
from src.app import ChatRoomApp

# Set the LDAP server and CA parameters
host = 'ldap://chatsec'
port = 389
bind_dn = 'cn=Manager,dc=chatsec,dc=com'
bind_password = 'root'
ca_cert_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/root/ca.crt'
ca_key_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/root/ca.key'
open_ssl_path = "C:/Program Files/OpenSSL-Win64/bin/openssl.exe"

# Create an LDAP client and a SSL client
ldap_client = LDAPClient(host, port, ca_cert_path, bind_dn, bind_password)
ssl_client = OpenSSLClient(open_ssl_path, ca_cert_path, ca_key_path)

# Create the app
app = ChatRoomApp(ldap_client, ssl_client)

# Create and add a chat room 
chatroom = Room(app, "Security Chat Room")
app.add_chat_room(chatroom)

# Create and add users
alice = User('cn=Alice,ou=Users,dc=chatsec,dc=com', 'alicepass', ldap_client, ssl_client)
bob = User('cn=Bob,ou=Users,dc=chatsec,dc=com', 'bobpass', ldap_client, ssl_client)
app.add_user(alice)
app.add_user(bob)

# Alice and Bob can now send and receive messages in the chatroom
alice_message = Message(alice, 'Hello Bob!')
bob.receive_message(alice_message)
bob_message = Message(bob, 'Hi Alice! How are you?')
alice.receive_message(bob_message)

app.run()

# Alice can leave the chatroom and Bob can delete her account
chatroom.remove_user(alice)
ldap_client.delete_user(alice)
