from re import sub as regex_replace
from re import match as regex_match


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "valid_domain": self.valid_domain,
            "valid_ip": self.valid_ip,
            "check_email": self.check_email,
            "le_domains_changed": self.le_domains_changed,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace(r'[^0-9a-zA-Z\.]+', '', key.replace(' ', '_'))

    @staticmethod
    def valid_domain(domain: str) -> bool:
        expr = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
        return True if regex_match(expr, domain) is not None else False

    @staticmethod
    def valid_ip(ip: str) -> bool:
        expr_ipv4 = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        expr_ipv6 = r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$'

        if regex_match(expr_ipv4, ip) is not None or regex_match(expr_ipv6, ip) is not None:
            return True

        return False

    @staticmethod
    def check_email(certs: dict) -> bool:
        for settings in certs.values():
            if 'email' not in settings or settings['email'] in ['', ' ', None, 'null', 'None']:
                return False

        return True

    @staticmethod
    def le_domains_changed(running_config: str, cert_key: str, config_domains: list) -> bool:
        changed = False
        run_domains = []

        for non_domain in ['_', '*']:
            # removing wildcards
            try:
                config_domains.remove(non_domain)
            except ValueError:
                pass

        block_started = False
        for line in running_config.split('\n'):
            if block_started:
                if line.find('Domains:') != -1:
                    run_domains = line.split(': ')[1].split(' ')
                    break

            elif line.find(f"Certificate Name: {cert_key}") != -1:
                block_started = True

        # checking if any domain was added
        for domain in config_domains:
            if domain not in run_domains:
                changed = True
                break

        if not changed:
            # checking if any domain was removed
            for domain in run_domains:
                if domain not in config_domains:
                    changed = True
                    break

        return changed
