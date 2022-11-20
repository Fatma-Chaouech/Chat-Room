# Chat-Room
## Description
A Chat-Room solution that respects security and cryptographic mechanisms by: 
* Validating users' identity and their authentication using LDAP.
* Using PKI to ensure authentication, integrity, confidentiality and non-repudiation of documents exchanged between partners.
* Using a trusted authority who must validate the electronic certificates of the different users.
* Managing certificates' life cycle.
## LDAP
### Basic Terms
* Short form of Lightweight Directory Acces Protocol.
* LDAP contains information related to users, groups and devices.
* In order not to use the existing schema, LDIF can be user (LDAP Data Interchange Format).
* LDAP is based on the idea of a tree data structure.
* The root contains DCs, which are Domain Components.
* The second level is for OUs, which stand for Organizational Units (i.e. groups or people)
* The third level contains the tree's leafs. Those leafs present entries for the actual data, where CN stands for Common Name, and the UID is the User Identifier.
* A DN (Distinguished Name) for an entry can be known by starting from the entry, traversing up the tree until hitting the root.
## Public Key Infrastructure
Public key infrastructure affirms the usage of a public key. It usually consists of the following components:

* A digital certificate also called a public key certificate
* Private Key tokens
* Registration authority
* Certification authority
* CMS or Certification management system
    
### Protocol Sequence
![image](https://user-images.githubusercontent.com/69005550/202903860-3e02fece-845c-4fb4-a225-28302192ec66.png)

## References
[LDAP](https://soshace.com/integrate-ldap-authentication-with-flask/)

[PKI](https://www.geeksforgeeks.org/public-key-infrastructure/)

[Openldap Server Configuration](https://computingforgeeks.com/install-and-configure-openldap-server-ubuntu/)
## To Check
[TLS/SSL](https://snyk.io/blog/implementing-tls-ssl-python/)

