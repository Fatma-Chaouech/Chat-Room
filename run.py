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
host = 'ldap://localhost'
port = 389
bind_dn = 'cn=Manager,dc=chatsec,dc=com'
bind_password = 'root'
ca_cert_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/root/ca.crt'
ca_key_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/root/ca.key'
open_ssl_path = "C:/Program Files/OpenSSL-Win64/bin/openssl.exe"
hostname = host + ':' + str(port)
client_cert_file = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/server/signed_certificate.pem'
client_key_file = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/server/private_key.pem'

# Set the certificates and keys paths
chatroom_keys_path = './chatroom_keys'
certs_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/certificates'
keys_path = 'C:/Users/Fatma/OneDrive/Desktop/Chat-Room/keys'

# Define the CA
ca = CertificateAuthority(open_ssl_path, ca_cert_path, ca_key_path, hostname)

print("CA created")
# Create an LDAP client and connect to the LDAP server
ldap_client = LDAPClient(host, port, ca, bind_dn, bind_password, client_cert_file, client_key_file)

print("LDAP client created")
# Create the app
app = ChatRoomApp(ldap_client, chatroom_keys_path, certs_path, keys_path)

print("App created")
# Add a chat room 
app.add_chat_room("IT Talk")
# app.add_chat_room("Express Your Feelings")
# app.add_chat_room("Sports Talk")

# Create users
alice = User(ca, ldap_client, 'Alice', 'alice123', certs_path, keys_path, organizational_unit="Unit", organization="Org", state="Alice-State", country="Alice-Country", email_address="alice@chatsec.com", common_name="Alice")



# Add users
app.add_user(alice, True)
print("User added")


# Send message
alice.send_message("IT Talk", "Hello, I'm Alice")

print("Starting app...")
app.start()
