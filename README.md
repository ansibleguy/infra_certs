# Ansible Role - Certificate Generator

Ansible Role to create certificates to use on a linux server.

[![Lint](https://github.com/O-X-L/ansible-role-certs/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/ansible-role-certs/actions/workflows/lint.yml)
[![Ansible Galaxy](https://badges.oss.oxl.app/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/oxlorg/certs)

**Molecule Integration-Tests**:

* Status: [![Molecule Test Status](https://badges.oss.oxl.app/infra_certs.molecule.svg)](https://github.com/O-X-L/ansible-role-oxl-cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2) |
[![Functional-Tests](https://github.com/O-X-L/ansible-role-certs/actions/workflows/integration_test_result.yml/badge.svg)](https://github.com/O-X-L/ansible-role-certs/actions/workflows/integration_test_result.yml)
* Logs: [API](https://ci.oss.oxl.app/api/job/ansible-test-molecule-infra_certs/logs?token=2b7bba30-9a37-4b57-be8a-99e23016ce70&lines=1000) | [Short](https://badges.oss.oxl.app/log/molecule_infra_certs_test_short.log) | [Full](https://badges.oss.oxl.app/log/molecule_infra_certs_test.log)

Internal CI: [Tester Role](https://github.com/O-X-L/ansible-role-oxl-cicd) | [Jobs API](https://github.com/O-X-L/github-self-hosted-jobs-systemd)


**Tested:**
* Debian 11
* Debian 12

----

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/O-X-L/ansible-role-certs

# from galaxy
ansible-galaxy install oxlorg.certs

# or to custom role-path
ansible-galaxy install oxlorg.certs --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

----

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
        domains: ['myRandomSite.net', 'oxl.at']
        email: 'certs@template.oxl.at'
    service: 'apache'
```

Example for Self-Signed config:

```yaml
certs:
  mode: 'selfsigned'  # or 'snakeoil' (if faster)
  # choose 'ca' instead if you use dns-names
  #   some browsers won't let you connect when using self-signed ones
  path: '/etc/nginx/ssl'
  group_key: 'nginx'
  owner_cert: 'nginx'
  cert:
    cn: 'My great certificate!'
    org: 'AnsibleGuy'
    country: 'AT'
    email: 'certs@template.oxl.at'
    domains: ['mySoGreat.site', 'oxl.at']
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
    email: 'certs@template.oxl.at'
    domains: ['mySoGreat.site', 'oxl.at']
  ca:
    path: '/etc/ca'
    cn: 'SUPER CertificateAuthority'
    org: 'AnsibleGuy'
    country: 'AT'
    email: 'certs@template.oxl.at'
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

----

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

----

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in [the main defaults-file](https://github.com/O-X-L/ansible-role-certs/blob/latest/defaults/main/1_main.yml)!


* **Note:** If you have the need to **mass manage certificates** - you might want to check out the [oxlorg.pki](https://github.com/O-X-L/ansible-role-pki) role that enables you to create and manage a full **P**ublic **K**ey **I**nfrastructure.


* **Note:** The certificate file-name (_name variable as defined or else CommonName_) will be updated:
  * spaces are transformed into underlines
  * all Characters except "0-9a-zA-Z." are removed
  * the file-extension (_crt/chain.crt/key/csr_) will be appended


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** For LetsEncrypt renewal to work, you must allow outgoing connections to:

  80/tcp, 443/tcp+udp to acme-v02.api.letsencrypt.org, staging-v02.api.letsencrypt.org (_debug mode_) and r3.o.lencr.org
