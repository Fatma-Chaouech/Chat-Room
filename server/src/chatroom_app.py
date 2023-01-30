from user import User
from room import Room
import time
from message import Message
from ast import parse
import sys
from json import dumps, loads

from rabbitmq import RabbitMq
sys.path.insert(0, './src')


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
        self.room_queues = []
        self.exchange = None

    def add_user(self, ch, method, properties, body):

        body = loads(body)
        username = body['username']
        password = body['password']
        print('Usernames logged in : ', self.users.keys())
        if (username in self.users.keys()) | (len(username) == 0):
            response = {'status': 'error',
                        'message': 'Choose another username'}
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            user = User(self.ldap_client.CA, self.ldap_client, username, password, self.certs_path, self.keys_path, organizational_unit="Unit",
                        organization="Org", state="State", country="Country", email_address=username+"@chatsec.com", common_name="Chatsec")
            ldap_response = self.ldap_client.add_user(user)
            if ldap_response == False:
                response = {'status': 'error', 'message': 'Server Error'}
                ch.basic_nack(delivery_tag=method.delivery_tag)

            else:
                response = {'status': 'success', 'message': 'Sucessfully logged in',
                            'certificate': user.get_certificate_path()}
                ch.basic_ack(delivery_tag=method.delivery_tag)
                self.users[username] = user
        ch.basic_publish(exchange='', routing_key=username,
                         body=dumps(response))

    def send_message(self, ch, method, properties, body):
        user, room_name, message = self._get_data(body, properties)
        print('Received message from user : ', user.name,
              ' in room : ', room_name, ' message : ', message)
        user.send_message(room_name, message, user.name)
        routing_key = '*.' + room_name.replace(' ', '')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.rabbitmq_client.channel.basic_publish(exchange='messaging', routing_key=routing_key, body=dumps({
                                                   'sender': user.name, 'content': message}))

    def select_room(self, ch, method, properties, body):
        user, room_name, _ = self._get_data(body, properties)
        self.chat_rooms[room_name].join(user)
        queue_name = (user.name + '.' + room_name).replace(' ', '')
        if not self.exchange:
            self.exchange = self.rabbitmq_client.channel.exchange_declare(
                exchange='messaging', exchange_type='topic')
        if queue_name not in self.room_queues:

            # create queue
            self.rabbitmq_client.channel.queue_declare(
                queue=queue_name, durable=True)
            # bind queue to exchange
            self.rabbitmq_client.channel.queue_bind(
                exchange='messaging', queue=queue_name, routing_key='*.'+room_name.replace(' ', ''))
            self.room_queues.append(queue_name)
        print('User joined room : ', user.name, room_name)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def add_chat_room(self, chat_name):
        chat_room = Room(chat_name, self.chatroom_keys_path)
        self.chat_rooms[chat_name] = chat_room

    def _get_data(self, body, properties):
        body = loads(body)
        username = body['sender']
        room_name = body['room_name']
        message = body['content']
        user = self.users[username]
        certificate = properties.headers['certificate']
        result = user.verify_certificate(certificate)
        if not result:
            raise Exception('Certificate not verified')
        return user, room_name, message

    def run(self):
        print('Server Listening ...')
        self.rabbitmq_client.channel.basic_consume(
            queue='login', on_message_callback=self.add_user)
        self.rabbitmq_client.channel.basic_consume(
            queue='room_selection', on_message_callback=self.select_room)
        self.rabbitmq_client.channel.basic_consume(
            queue='messaging', on_message_callback=self.send_message)
        self.rabbitmq_client.channel.start_consuming()
