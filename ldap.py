from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError

ldsp_server = f"ldap://localhost:389"

root_dn = "dc=example, dc=org"

ldap_user_name = 'admin'
ldap_password = 'admin'

user = f'cn={ldap_user_name}, root_dn'


def global_ldap_authentication(user_name, user_pwd):
	
	server_name = ""
	ldap_user_name = user_name.strip()
	ldap_user_pwd = user_pwd.strip()
	#tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
	server = Server(f'ldap://{server_name}:389')#,user_ssl=True)#,tls=tls_configuration)
	conn = Connection(server, user=ldap_user_name, password=ldap_user_pwd, authentication='NTLM', auto_referrals=False)
	if not conn.bind():
		print(f'Cannot bind to ldap server: {conn.last_error}')
	else:
		print(f'Successful bind to ldap server')
	return

global_ldap_authentication(ldap_user_name, ldap_password)
                                       
