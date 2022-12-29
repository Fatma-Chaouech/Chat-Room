import sys
sys.path.insert(0,'./src')
import threading
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
        self.lock = threading.Lock()
        self.openssl_client = OpenSSLClient(CA, self, certs_path, keys_path)
        self.__authenticate(self)
        self.__create_certificate(self)
        

    def __authenticate(self):
        try :
            self.ldap_client.authenticate(self.name, self.password)
        except Exception as e:
            print(e)

    def __create_certificate(self):
        csr_path = './requests/{}_csr.pem'.format(self.name)
        self.openssl_client.verify_certificate(csr_path)

    # Will be invoked by the chat room when we add user to it
    def define_room(self, chat_room):
        self.chat_rooms[chat_room.name] = chat_room
        self.last_received_ids[chat_room.name] = 0

    def send_message(self, room_name, message):
        self.chat_rooms[room_name].send_message(self, message)

    def get_messages(self, room_name):
        with self.lock:
            messages = self.chat_rooms[room_name].get_messages(self.last_received_ids[room_name])
            self.last_received_ids[room_name] += len(messages)
            return messages

