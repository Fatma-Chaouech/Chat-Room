import socket
import ssl
import subprocess


class OpenSSLClient:
    def __init__(self, CA, user, certs_path, keys_path, csr_path):
        self.CA = CA
        self.user = user
        self.tls_certificate = None
        self.certs_path = certs_path
        self.cert_path = str(certs_path) + '\\' + user.name.lower() + '.pem'
        self.key_path = str(keys_path) + '\\' + user.name.lower() + '.pem'
        self.__generate_tls_certificate(csr_path)
        self.__create_secure_client_socket(CA.hostname)

    def __create_csr(self, csr_path):
        subprocess.run([
            self.CA.openssl_path, 'req', '-new', '-out', csr_path, '-passout', 'pass:' + self.user.name + 'Client', '-keyout', self.key_path,
            '-subj', '/C={}'.format(self.user.country),
            '-subj', '/ST={}'.format(self.user.state),
            '-subj', '/O={}'.format(self.user.organization),
            '-subj', '/OU={}'.format(self.user.organizational_unit),
            '-subj', '/CN={}'.format(self.user.common_name),
            '-subj', '/emailAddress={}'.format(self.user.email_address)
        ])
        print("Creating CSR for user {} to path {}".format(self.user.name, csr_path))


    
    
    def __generate_tls_certificate(self, csr_path):
        # Generate a new TLS certificate by first generating a CSR, then signing it using the CA's private key
        self.__create_csr(csr_path)
        self.tls_certificate = self.CA.sign_csr(csr_path, self.cert_path)
        print("TLS certificate for user {} generated".format(self.user.name))
    
    def verify_certificate(self, certificate_path):
        try:
            result = subprocess.run(['openssl', 'verify', '-CAfile', self.CA.ca_cert_path, certificate_path], capture_output=True)
            error = result.stderr.decode('utf-8').strip()
            if len(error) > 0:
                return False
            return True
        except subprocess.CalledProcessError as e:
            return False

    def __create_ssl_context(self):
        # Create an SSL context object and configure it to use the CA's certificate, the client's certificate and private key,
        # and the required SSL/TLS protocols and cipher suites
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_verify_locations(self.CA.ca_cert_path)
        ssl_context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path, password=self.user.name + 'Client')
        ssl_context.set_ciphers("ECDHE-RSA-AES256-SHA384:AES256-SHA256")
        return ssl_context
    
    def __create_secure_client_socket(self, server_hostname):
        # Create a TCP socket and then wrap it in an SSL/TLS layer using the SSL context created earlier
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_context = self.__create_ssl_context()
        return ssl_context.wrap_socket(client_socket,server_hostname=server_hostname)

    def get_certificate_path(self):
        return self.cert_path
    
    def get_certificate(self):
        certificate = open(self.cert_path, "rb").read()
        return certificate
