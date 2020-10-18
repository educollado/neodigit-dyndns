import requests
import json
import yaml

#Read the config file
def read_config(file):
    # This funcions reads config.cfg and extracts token, domain and subdomain
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        return(data['token'],data['my_domain'],data['my_subdomain'])

def check_domain_registrar(my_domain,headers,domain):
    # Checks if the domain is in Neodigit and downloads domain list
    r = requests.get('https://api.neodigit.net/v1/domains/domains', headers=headers, verify=True)
    domains = json.loads(r.text)
    for i in domains:
        if ((i['product_info']['product_status']) == 'active' and i['name'] == my_domain):
            return("\u2611 Your domain {} is registered in Neodigit".format(my_domain))
        return("\u2612 Your domain {} is not registered in Neodigit".format(my_domain))

def obtain_subdomain_id(my_subdomain,headers,domain_id):
    # Obtain domain and subdomain Id from the Neodigit's API
    url_domain='https://api.neodigit.net/v1/dns/zones/' + domain_id + '/records'
    r = requests.get(url_domain, headers=headers, verify=True)
    j = json.loads(r.text)
    for i in j:
        if i['name'] == my_subdomain and i['type'] == 'A':
            return([i['id'], i['content']])
    return([None, None])
    

def obtain_domain_id(my_subdomain,my_domain,header,domains):
    # Obtaining domain Id from neodigit's API
    for i in domains:
        if i['name'] == my_domain:       
            domain_id = str((i['id']))
            subdomain_info = (obtain_subdomain_id(my_subdomain,header,domain_id)) 
            subdomain_id = subdomain_info[0]
            subdomain_ip = subdomain_info[1]
            return({'domain_id': domain_id, 'subdomain_id': subdomain_id, 'subdomain_ip': subdomain_ip})
    return({'domain_id': None, 'subdomain_id': None, 'subdomain_ip': None})

def obtain_my_ip():
    # Obtain my ip using ipfy API
    return(json.loads(requests.get('https://api.ipify.org?format=json').text)['ip'])
    #return('8.8.8.8')
    
def update_ip(headers,token,domain_info,current_ip):
    # Update A record in existing DNS entry
    headers_update = { 'X-TCpanel-Token' : token, 'Content-Type': 'application/json'}
    domain_id = str(domain_info['domain_id'])
    subdomain_id = str(domain_info['subdomain_id'])
    url_change_ip='https://api.neodigit.net/v1/dns/zones/' + domain_id + '/records/' + subdomain_id
    updated_data={"record": { "content" : current_ip}}
    data=json.dumps(updated_data)
    response = requests.put(url_change_ip, data=data, headers=headers_update, verify=True)
    return(response)

def create_registry(my_subdomain,headers,token,domain_info, current_ip):
    # Create DNS entry in Neodigit's DNS
    headers_update = { 'X-TCpanel-Token' : token, 'Content-Type': 'application/json'}
    domain_id = str(domain_info['domain_id'])
    subdomain_id = str(domain_info['subdomain_id'])
    url_change_ip='https://api.neodigit.net/v1/dns/zones/' + domain_id + '/records'
    updated_data={"record":{"name": my_subdomain ,"type":"A","content": current_ip ,"ttl":60}}
    data=json.dumps(updated_data)
    response = requests.post(url_change_ip, data=data, headers=headers_update, verify=True)
    return(response)  

