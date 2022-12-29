import subprocess
import threading

class Room:
    def __init__(self, name, chatroom_key_path):
        self.key_path = chatroom_key_path + '/' + name + '.pem'
        self.name = name
        self.users = []
        self.messages = []
        self.lock = threading.Lock()
        self.__generate_key()

    def __generate_key(self):
        return  subprocess.run([
        'openssl', 'genrsa', '-out', self.key_path, '2048'
        ])

    def join(self, user):
        self.__add_user(user)
        self.send_message(user.name, " has joined the room.")

    def leave(self, user_name):
        self.__remove_user(user_name)
        self.send_message(user_name, " has left the room.")

    def __add_user(self, user):
        with self.lock:
            self.users[user.name] = user
            user.define_room(self)

    def __remove_user(self, user_name):
        with self.lock:
            self.users.pop(user_name)

    def send_message(self, message):
        with self.lock:
            self.messages.append(message)

    def get_messages(self, last_received_id):
        with self.lock:
            return self.messages[last_received_id:]

    