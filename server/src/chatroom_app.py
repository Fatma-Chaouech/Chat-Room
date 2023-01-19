from ast import parse
import sys
from json import dumps, loads

from rabbitmq import RabbitMq
sys.path.insert(0,'./src')
from message import Message
import time
from room import Room
from user import User

class ChatRoomApp:
    def __init__(self, ldap_client, chatroom_keys_path, certs_path, keys_path):
        self.ldap_client = ldap_client
        self.chat_rooms = {}
        self.users = {}
        self.certs_path = certs_path
        self.keys_path = keys_path
        self.chatroom_keys_path = chatroom_keys_path
        self.rabbitmq_client = RabbitMq()
        self.ldap_client.connect()


    def add_user(self, ch, method, properties, body):
        
        body = loads(body)
        username = body['username']
        password = body['password']
        print('Usernames logged in : ', self.users.keys())
        if (username in self.users.keys()) | (len(username) == 0):
            response = {'status' : 'error', 'message' : 'Choose another username'}
            ch.basic_nack(delivery_tag=method.delivery_tag)        
        else : 
            user = User(self.ldap_client.CA, self.ldap_client, username, password, self.certs_path, self.keys_path, organizational_unit="Unit", organization="Org", state="State", country="Country", email_address=username+"@chatsec.com", common_name="Chatsec")
            ldap_response = self.ldap_client.add_user(user)
            if ldap_response == False:
                response = {'status' : 'error', 'message' : 'Server Error'}
                ch.basic_nack(delivery_tag=method.delivery_tag)        

            else :
                response = {'status' : 'success', 'message' : 'Sucessfully logged in'}
                ch.basic_ack(delivery_tag=method.delivery_tag)        
                self.users[username] = user
        ch.basic_publish(exchange='', routing_key=username, body=dumps(response))

            

    def add_chat_room(self, chat_name):
        chat_room = Room(chat_name, self.chatroom_keys_path)
        
        self.chat_rooms[chat_name] = chat_room



    def run(self):
        print('Server Listening ...')
        self.rabbitmq_client.channel.basic_consume(queue='login', on_message_callback=self.add_user)
        self.rabbitmq_client.channel.start_consuming()
        print('User successfully logged in')

