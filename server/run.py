# Import the necessary classes and functions
from pathlib import Path
import sys
sys.path.insert(0,'./src')
from src.certificate_authority import CertificateAuthority
from src.room import Room
from src.ldap_client import LDAPClient
from src.user import User
from src.message import Message
from src.chatroom_app import ChatRoomApp


def relative_to_root(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent
    return ASSETS_PATH / Path(path)

# Set the LDAP server and CA parameters
host = 'ldap://localhost'
port = 389
bind_dn = 'cn=Manager,dc=chatsec,dc=com'
bind_password = 'root'
ca_cert_path = relative_to_root('generated_files\\root\\ca.crt')
ca_key_path = relative_to_root('generated_files\\root\\ca.key')
open_ssl_path = "C:/Program Files/OpenSSL-Win64/bin/openssl.exe"
hostname = host + ':' + str(port)
client_cert_file = relative_to_root('generated_files\\server_keys\\signed_certificate.pem')
client_key_file = relative_to_root('generated_files\\server_keys\\private_key.pem')

# Set the certificates and keys paths
chatroom_keys_path = relative_to_root('generated_files\\chatroom_keys')
certs_path = relative_to_root('generated_files\\certificates')
keys_path = relative_to_root('generated_files\\users_keys')

# Define the CA
ca = CertificateAuthority(open_ssl_path, ca_cert_path, ca_key_path, hostname)

# Create an LDAP client and connect to the LDAP server
ldap_client = LDAPClient(host, port, ca, bind_dn, bind_password, client_cert_file, client_key_file)

# Create the app
chatroom_app = ChatRoomApp(ldap_client, chatroom_keys_path, certs_path, keys_path)

# Add a chat room 
chatroom_app.add_chat_room("Philosophy")
chatroom_app.add_chat_room("News")
chatroom_app.add_chat_room("IT Talk")
chatroom_app.add_chat_room("ChatGPT")
chatroom_app.add_chat_room("All About Life")
chatroom_app.add_chat_room("Need Help")

print("Server Started.")
chatroom_app.run()