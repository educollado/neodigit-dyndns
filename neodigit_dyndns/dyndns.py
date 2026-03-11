import requests
import json
import yaml


def read_config(file):
    """Read config file and extract token, domain and subdomain."""
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data['token'], data['my_domain'], data['my_subdomain']


def check_domain_registrar(my_domain, headers):
    """Check if the domain is registered in Neodigit."""
    r = requests.get('https://api.neodigit.net/v1/domains/domains', headers=headers, verify=True)
    for i in r.json():
        if i['product_info']['product_status'] == 'active' and i['name'] == my_domain:
            return "\u2611 Your domain {} is registered in Neodigit".format(my_domain)
    return "\u2612 Your domain {} is not registered in Neodigit".format(my_domain)


def obtain_subdomain_id(my_subdomain, headers, domain_id):
    """Obtain subdomain record ID and current IP from the Neodigit API."""
    url = 'https://api.neodigit.net/v1/dns/zones/' + domain_id + '/records'
    r = requests.get(url, headers=headers, verify=True)
    for i in r.json():
        if i['name'] == my_subdomain and i['type'] == 'A':
            return [i['id'], i['content']]
    return [None, None]


def obtain_domain_id(my_subdomain, my_domain, headers, domains):
    """Obtain domain and subdomain info from the Neodigit API."""
    for i in domains:
        if i['name'] == my_domain:
            domain_id = str(i['id'])
            subdomain_info = obtain_subdomain_id(my_subdomain, headers, domain_id)
            return {
                'domain_id': domain_id,
                'subdomain_id': subdomain_info[0],
                'subdomain_ip': subdomain_info[1],
            }
    return {'domain_id': None, 'subdomain_id': None, 'subdomain_ip': None}


def obtain_my_ip():
    """Obtain the current public IP using the ipify API."""
    return requests.get('https://api.ipify.org?format=json').json()['ip']


def update_ip(headers, domain_info, current_ip):
    """Update the A record in an existing DNS entry."""
    headers_update = {**headers, 'Content-Type': 'application/json'}
    domain_id = str(domain_info['domain_id'])
    subdomain_id = str(domain_info['subdomain_id'])
    url = 'https://api.neodigit.net/v1/dns/zones/' + domain_id + '/records/' + subdomain_id
    data = json.dumps({"record": {"content": current_ip}})
    return requests.put(url, data=data, headers=headers_update, verify=True)


def create_registry(my_subdomain, headers, domain_info, current_ip):
    """Create a new DNS A record in Neodigit."""
    headers_update = {**headers, 'Content-Type': 'application/json'}
    domain_id = str(domain_info['domain_id'])
    url = 'https://api.neodigit.net/v1/dns/zones/' + domain_id + '/records'
    data = json.dumps({"record": {"name": my_subdomain, "type": "A", "content": current_ip, "ttl": 60}})
    return requests.post(url, data=data, headers=headers_update, verify=True)
