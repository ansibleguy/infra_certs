from re import sub as regex_replace
from re import match as regex_match


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "valid_domain": self.valid_domain,
            "valid_ip": self.valid_ip,
            "check_email": self.check_email,
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

