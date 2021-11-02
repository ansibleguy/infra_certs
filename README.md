# Ansible Role for certificate generation

**Tested:**
* Debian 11

## Functionality

* Package installation
  * Ansible dependencies (_minimal_)
  * 
* Configuration
  * Two Possible Modes
    * Generate Self-Signed certificate
    * Create an internal-ca and generate certificates using it
  * Default config:
    * Mode => Self-Signed
  * Default opt-ins:
    * 
  * Default opt-outs:
    * 


## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!



## Requirements

* Community collection: ```ansible-galaxy install -r requirements.yml```


## Usage

Define the config as needed:

```yaml
app:

```

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* base => only configure basics; sites will not be touched
* sites
* config
* certs
