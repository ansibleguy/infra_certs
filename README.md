# Ansible Role - Certificate Generator

Ansible Role to create certificates to use on a linux server.

[![Molecule Test Status](https://badges.ansibleguy.net/infra_certs.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_certs.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_certs.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_certs.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://img.shields.io/ansible/role/56802)](https://galaxy.ansible.com/ansibleguy/infra_certs)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F56802%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/infra_certs)


**Tested:**
* Debian 11

## Install

```bash
ansible-galaxy install ansibleguy.infra_certs

# or to custom role-path
ansible-galaxy install ansibleguy.infra_certs --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

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


  * **Default config**:
    * Mode => Self-Signed


## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Note:** If you have the need to mass manage certificates - you might want to check out the [ansibleguy.infra_pki](https://github.com/ansibleguy/infra_pki) role that enables you to create and manage a full **P**ublic **K**ey **I**nfrastructure.


* **Note:** The certificate file-name (_name variable as defined or else CommonName_) will be updated:
  * spaces are transformed into underlines
  * all Characters except "0-9a-zA-Z." are removed
  * the file-extension (_crt/chain.crt/key/csr_) will be appended


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** For LetsEncrypt renewal to work, you must allow outgoing connections to:

  80/tcp, 443/tcp+udp to acme-v02.api.letsencrypt.org, staging-v02.api.letsencrypt.org (_debug mode_) and r3.o.lencr.org


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
  # choose 'ca' instead if you use dns-names
  #   some browsers won't let you connect when using self-signed ones
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

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
