"""
This package checks your public IPv4 and updates your DNS entry in the
neodigit.net DNS panel.

You need a config file with token, domain and subdomain.

Usage: python -m neodigit_dyndns <config_file>
"""
import sys
import requests

from .dyndns import read_config, check_domain_registrar, obtain_domain_id, obtain_my_ip, create_registry, update_ip


def main():
    if len(sys.argv) < 2:
        print("Usage: neodigit-dyndns <config_file>")
        sys.exit(1)

    file = sys.argv[1]
    token, my_domain, my_subdomain = read_config(file)
    headers = {'X-TCpanel-Token': token}

    print(check_domain_registrar(my_domain, headers))

    r = requests.get('https://api.neodigit.net/v1/dns/zones', headers=headers, verify=True, params={'status': 'active'})
    domains = r.json()
    domain_info = obtain_domain_id(my_subdomain, my_domain, headers, domains)
    current_ip = obtain_my_ip()

    if domain_info['domain_id'] is None:
        print("\u2612 The domain {} is not in your account.".format(my_domain))
    elif domain_info['subdomain_id'] is None:
        print("\u2611 The domain {} has no subdomain {}, creating it now.".format(my_domain, my_subdomain))
        create_registry(my_subdomain, headers, domain_info, current_ip)
    else:
        if domain_info['subdomain_ip'] == current_ip:
            print("\u2611 Your current IP has not changed: {}".format(current_ip))
        else:
            print('\u2611 Your IP has changed from {} to {}'.format(domain_info['subdomain_ip'], current_ip))
            update_ip(headers, domain_info, current_ip)


if __name__ == '__main__':
    main()
