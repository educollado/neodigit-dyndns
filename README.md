# Dynamic Dns with Neodigit's API

![GitHub](https://img.shields.io/github/license/educollado/neodigit-dyndns)
![GitHub last commit](https://img.shields.io/github/last-commit/educollado/neodigit-dyndns)
![GitHub repo size](https://img.shields.io/github/repo-size/educollado/neodigit-dyndns)
![Twitter Follow](https://img.shields.io/twitter/follow/ecollado)
![Mastodon Follow](https://img.shields.io/mastodon/follow/72314?domain=https%3A%2F%2Fmastodon.social&style=social)

## TESTING PURPOSES ONLY

## Links

* Github: https://github.com/educollado/neodigit-dyndns
* Pypi.org: https://pypi.org/project/neodigit-dyndns/

dynamic_dns for Neodigit domains

https://panel.neodigit.net

## Configuration: 

You need to configure the config.cfg and pass it the file as attribute 

* token: 
* my_domain: 
* my_subdomain: 

You can obtain your own token Id from: https://panel.neodigit.net/api-consumers 

ie: our token is 1234, and our subdomain is test.mydomain.com. This file is a YAML file.

* token: 1234 
* my_domain: mydomain.com 
* my_subdomain: test 

## Instalation from source

```bash
git clone https://github.com/educollado/neodigit-dyndns.git
```

For this script you need requests as you can see in the code: 

```bash
pip install requests
```

Or maybe you can use the requirements.txt file:

```bash
pip install -r requirements.txt
```

One interesting step is to add to your crontab: 

```bash
0,15,30,45 * * * * python3 /path-to/neodigit-dyndns/neodigit_dyndns /url/to/config.cfg > /dev/null 2>&
```

## Instalation from PiP

```bash
pip install neodigit-dyndns
```
https://pypi.org/project/neodigit-dyndns/

## Neodigit API
API Documentation: https://developers.neodigit.net/

## License
[GPL3](https://github.com/educollado/neodigit-dyndns/blob/main/LICENSE)
