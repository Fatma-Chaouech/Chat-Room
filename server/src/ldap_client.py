import ldap3
import ssl

class LDAPClient:
    def __init__(self, host, port, CA, bind_dn, bind_password, client_cert_file, client_key_file):
        self.host = host
        self.port = port
        self.CA = CA
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.conn = None
        self.client_cert_file = client_cert_file
        self.client_key_file = client_key_file

    def connect(self):
        
        tls = ldap3.Tls(validate=ssl.CERT_REQUIRED, ca_certs_file=self.CA.ca_cert_path, local_certificate_file=self.client_cert_file, local_private_key_file=self.client_key_file)
        server = ldap3.Server(host=self.host, port=self.port, use_ssl=True, tls=tls)
        self.conn = ldap3.Connection(server=server, user=self.bind_dn, password=self.bind_password)
        self.conn.open()
        self.conn.bind()
        print('Connected to LDAP server.')

    def disconnect(self):
        if self.conn and self.conn.bound:
            self.conn.unbind()
            self.conn.close()
            self.conn = None

    def add_user(self, user):
        dn = 'cn=Fatma,dc=chatsec,dc=com'
        attrs = {
            'objectClass': 'person',
            'sn': user.name,
            'userPassword': user.password,
        }
        
        if not self.conn or not self.conn.bound:
            self.connect()
        self.conn.add(dn=dn, attributes=attrs)
        return self.conn.result

    def delete_user(self, username):
        dn = 'cn=' + username + ',ou=users,dc=chatsec,dc=com'
        if not self.conn or not self.conn.bound:
            self.connect()
        self.conn.delete(dn=dn)
        return self.conn.result

    def verify_login(self, username, password):
        dn = 'cn=' + username + 'dc=chatsec,dc=com'
        try:
            self.conn.bind(dn=dn, password=password)
            return True
        except ldap3.core.exceptions.LDAPBindError:
            return False