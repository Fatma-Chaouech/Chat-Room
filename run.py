# Import the necessary classes and functions
import sys
sys.path.insert(0,'./src')
from certificate_authority import CertificateAuthority
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
hostname = host + ':' + str(port)

# Set the certificates and keys paths
chatroom_keys_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/chatroom_keys'
certs_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/certificates'
keys_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/keys'

# Define the CA
ca = CertificateAuthority(open_ssl_path, ca_cert_path, ca_key_path, hostname)

# Create an LDAP client and connect to the LDAP server
ldap_client = LDAPClient(host, port, ca, bind_dn, bind_password)

# Create the app
app = ChatRoomApp(ldap_client, chatroom_keys_path, certs_path, keys_path)

# Add a chat room 
app.add_chat_room("IT Talk")
app.add_chat_room("Express Your Feelings")
app.add_chat_room("Sports Talk")

# Create users
alice = User(ca, ldap_client, 'Alice', 'alice', certs_path, keys_path, organizational_unit="AliceOrgUnit", organization="AliceOrg", state="Alice-State", country="Alice-Country", email_address="alice@gmail.com", common_name="Alice")
bob = User(ca, ldap_client, 'Bob', 'bob', certs_path, keys_path, organizational_unit="BobOrgUnit", organization="BobOrg", state="Bob-State", country="Bob-Country", email_address="bob@gmail.com", common_name="Bob")
carol = User(ca, ldap_client, 'Carol', 'carol', certs_path, keys_path, organizational_unit="CarolOrgUnit", organization="CarolOrg", state="Carol-State", country="Carol-Country", email_address="carol@gmail.com", common_name="Carol")
dave = User(ca, ldap_client, 'Dave', 'dave', certs_path, keys_path, organizational_unit="DaveOrgUnit", organization="DaveOrg", state="Dave-State", country="Dave-Country", email_address="dave@gmail.com", common_name="Dave")


# Add users
app.add_user(alice)
app.add_user(bob)
app.add_user(carol)
app.add_user(dave)

# Send message
alice.send_message("IT Talk", "Hello, I'm Alice")
bob.send_message("IT Talk", "Hi Alice, are you a developer?")

app.start()
