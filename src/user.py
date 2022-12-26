import threading

class User:
    def __init__(self, ldap_client, openssl_client, name, password, cert_path=None):
        self.ldap_client = ldap_client
        self.openssl_client = openssl_client
        self.name = name
        self.password = password
        self.cert_path = cert_path
        self.last_received_id = 0
        self.lock = threading.Lock()

    def authenticate(self):
        return self.ldap_client.authenticate(self.name, self.password)

    def create_certificate(self):
        csr_path = './certificates/{}_csr.pem'.format(self.name)
        self.openssl_client.create_csr(csr_path, self.name, self.name, 'TN', 'Ben-Arous', 'Org', 'Unit')
        self.openssl_client.sign_csr(csr_path, self.cert_path)

    def send_message(self, message):
        self.chat_room.send_message(self, message)

    def get_messages(self):
        with self.lock:
            messages = self.chat_room.get_messages(self.last_received_id)
            self.last_received_id += len(messages)
            return messages

    def receive_message(self):
        data = self.client_socket.recv(1024)
        if not data:
            return None
        return data.decode('utf-8')
