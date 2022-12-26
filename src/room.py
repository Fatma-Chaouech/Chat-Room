import threading

class Room:
    def __init__(self, ldap_client, openssl_client, name, users=[]):
        self.ldap_client = ldap_client
        self.openssl_client = openssl_client
        self.name = name
        self.users = users
        self.messages = []
        self.lock = threading.Lock()

    def add_user(self, user):
        with self.lock:
            self.users.append(user)

    def remove_user(self, user):
        with self.lock:
            self.users.remove(user)

    def send_message(self, user, message):
        with self.lock:
            self.messages.append((user, message))

    def get_messages(self, last_received_id):
        with self.lock:
            return self.messages[last_received_id:]