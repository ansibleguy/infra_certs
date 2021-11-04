# Certificate Generator Role

**Tested:**
* Debian 11

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)
  * Crypto Dependencies


* **Configuration**
  * **Four Possible Modes**:
    * Generate **Self-Signed** certificate
    * Use a **minimal Certificate Authority** to create signed certificates
    * Configure **LetsEncrypt-Certbot** to generate publicly valid certificates
      * Supported for Nginx and Apache
      * Host needs to have a valid public dns record pointed at it
      * Needs to be publicly reachable over port 80/tcp
    * _Use a proper **Certificate Authority** (_full PKI_) to create **signed certificates**_ => not yet available


  * **Default config**:
    * Mode => Self-Signed


## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** The certificate file-name (_name variable as defined or else CommonName_) will be updated:
  * spaces are transformed into underlines
  * all Characters except "0-9a-zA-Z." are removed
  * the file-extension (_crt/chain.crt/key/csr_) will be appended

## Requirements

* Community collection: ```ansible-galaxy install -r requirements.yml```


## Usage

### Notes
The **self-signed and minimal-ca** modes will only create a single certificate per run.

Re-runs can save some overhead by using the 'certs' tag.


The **LetsEncrypt** mode will create/remove multiple certificates as defined.


### Config

Example for LetsEncrypt config:

```yaml
certs:
  mode: 'le_certbot'
  path: '/etc/apache2/ssl'
  letsencrypt:
    certs:
      myNiceSite:
        domains: ['myRandomSite.net', 'ansibleguy.net']
        email: 'certs@template.ansibleguy.net'
    service: 'apache'
```

Example for Self-Signed config:

```yaml
certs:
  mode: 'selfsigned'
  path: '/etc/nginx/ssl'
  group_key: 'nginx'
  owner_cert: 'nginx'
  cert:
    cn: 'My great certificate!'
    org: 'AnsibleGuy'
    country: 'AT'
    email: 'certs@template.ansibleguy.net'
    domains: ['mySoGreat.site', 'ansibleguy.net']
    ips: ['192.168.44.2']
    pwd: !vault ...
```

Example for minimal-CA config:

```yaml
certs:
  mode: 'ca'
  path: '/etc/ca/certs'
  mode_key: '0400'
  cert:
    name: 'custom_file_name'  # extension will be appended
    cn: 'My great certificate!'
    org: 'AnsibleGuy'
    country: 'AT'
    email: 'certs@template.ansibleguy.net'
    domains: ['mySoGreat.site', 'ansibleguy.net']
  ca:
    path: '/etc/ca'
    cn: 'SUPER CertificateAuthority'
    org: 'AnsibleGuy'
    country: 'AT'
    email: 'certs@template.ansibleguy.net'
    pwd: !vault ...
```

Using the minimal-CA you can create multiple certificates signed by the CA by re-running the role with changed 'cert' settings.


You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml --ask-vault-pass
```

There are also some useful **tags** available:
* certs => ignore ca tasks; only generate certs
* selfsigned
* config
* certs
