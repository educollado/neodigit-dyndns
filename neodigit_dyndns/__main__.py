import requests
import json
import sys

from dyndns import *
'''
This package checks your public ipv4 and updates your DNS entry in the 
neodigit.net DNS panel.

You need a token ID, a domain and a subdomain

'''
# Main Code
#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

file=str(sys.argv[1])
print(file)
config = (read_config(file))
token=config[0]
my_domain=config[1]
my_subdomain=config[2]
headers = { 'X-TCpanel-Token' : token}
parameters = {'status': 'active'}



print(check_domain_registrar(my_domain,headers,my_domain))


# Download DNS Zone list
r = requests.get('https://api.neodigit.net/v1/dns/zones', headers=headers, verify=True, params=parameters)
domains = json.loads(r.text)
domain_info = obtain_domain_id(my_subdomain,my_domain,headers,domains)
#domain_info = obtain_domain_id(domains)
current_ip = obtain_my_ip()

if (domain_info['domain_id'] == None):
    print("\u2612 The domain {} is not in your account.".format(my_domain))
if (domain_info['domain_id'] != None and domain_info['subdomain_id'] == None):
    print("\u2611 The domain {} has not defined subdomain {}, we are going to create it for you.".format(my_domain,my_subdomain))
    response = (create_registry(my_subdomain,headers,token,domain_info, current_ip))
if (domain_info['domain_id'] != None and domain_info['subdomain_id'] != None):
    if domain_info['subdomain_ip'] == current_ip:
        print("\u2611 Your current IP has not been changed: {}".format(current_ip))
    else:
        print('\u2611 Your old IP {} have been changed to the new one {}'.format(domain_info['subdomain_ip'],current_ip))
        response = (update_ip(headers,token,domain_info,current_ip))

