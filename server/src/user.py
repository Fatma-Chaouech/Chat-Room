import sys
import os
sys.path.insert(0,'./src')
from openssl_client import OpenSSLClient

class User:
    def __init__(self, CA, ldap_client, name, password, certs_path=None, keys_path=None,\
        organizational_unit='unit', organization='org', state='state', country='TN', email_address='user@gmail.com', common_name='common'):
        self.ldap_client = ldap_client
        self.name = name
        self.common_name = common_name
        self.email_address = email_address
        self.country = country
        self.state = state
        self.organization = organization
        self.organizational_unit = organizational_unit
        self.password = password
        self.chat_rooms = {}
        self.last_received_ids = {}
        csr_path = os.getcwd() + '\\generated_files\\requests\\{}_csr.pem'.format(self.name)
        self.openssl_client = OpenSSLClient(CA, self, certs_path, keys_path, csr_path)
        

    # Will be invoked by the chat room when we add user to it
    def define_room(self, chat_room):
        self.chat_rooms[chat_room.name] = chat_room
        self.last_received_ids[chat_room.name] = 0

    def send_message(self, room_name, message):
        self.chat_rooms[room_name].send_message(message)

    def get_messages(self, room_name):
        messages = self.chat_rooms[room_name].get_messages(self.last_received_ids[room_name])
        self.last_received_ids[room_name] += len(messages)
        return messages

    def reset_last_received_id(self, room_name):
        self.last_received_ids[room_name] = 0

