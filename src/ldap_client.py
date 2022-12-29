import ldap3
import ssl

class LDAPClient:
    def __init__(self, host, port, CA, bind_dn, bind_password):
        self.host = host
        self.port = port
        self.CA = CA
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.conn = None

    def connect(self):
        
        tls = ldap3.Tls(validate=ssl.CERT_REQUIRED, ca_certs_file=self.CA.ca_cert_path)
        server = ldap3.Server(host=self.host, port=self.port, use_ssl=True, tls=tls)
        self.conn = ldap3.Connection(server=server, auto_bind=ldap3.AUTO_BIND_TLS_BEFORE_BIND,  client_strategy=ldap3.SYNC, user=self.bind_dn, password=self.bind_password, authentication=ldap3.SIMPLE)
        self.conn.open()
        self.conn.bind()

    def disconnect(self):
        if self.conn and self.conn.bound:
            self.conn.unbind()
            self.conn.close()
            self.conn = None

    def add_user(self, user):
        dn = 'cn=' + user.name + ',ou=users,dc=chatsec,dc=com'
        attrs = {
            'objectClass': ['inetOrg', 'person'],
            'cn': user.name,
            'sn': user.name,
            'userPassword': user.password
        }
        if not self.conn or not self.conn.bound:
            self.connect()
        self.conn.add(dn=dn, object_class=attrs.keys(), attributes=attrs)
        return self.conn.result

    def delete_user(self, username):
        dn = 'cn=' + username + ',ou=users,dc=chatsec,dc=com'
        if not self.conn or not self.conn.bound:
            self.connect()
        self.conn.delete(dn=dn)
        return self.conn.result

    def verify_login(self, username, password):
        dn = 'cn=' + username + ',ou=users,dc=chatsec,dc=com'
        try:
            self.conn.bind(dn=dn, password=password)
            return True
        except ldap3.core.exceptions.LDAPBindError:
            return False