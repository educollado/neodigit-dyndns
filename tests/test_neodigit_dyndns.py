import json
from io import StringIO
from unittest.mock import MagicMock, mock_open, patch

import pytest

from neodigit_dyndns import __version__
from neodigit_dyndns.dyndns import (
    check_domain_registrar,
    create_registry,
    obtain_domain_id,
    obtain_my_ip,
    obtain_subdomain_id,
    read_config,
    update_ip,
)


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

def test_version():
    assert __version__ == '0.3.3'


# ---------------------------------------------------------------------------
# read_config
# ---------------------------------------------------------------------------

VALID_CONFIG = """
token: abc123
my_domain: example.com
my_subdomain: home
"""

def test_read_config_valid(tmp_path):
    cfg = tmp_path / "config.yml"
    cfg.write_text(VALID_CONFIG)
    token, domain, subdomain = read_config(str(cfg))
    assert token == 'abc123'
    assert domain == 'example.com'
    assert subdomain == 'home'

def test_read_config_missing_key(tmp_path):
    cfg = tmp_path / "config.yml"
    cfg.write_text("token: abc123\nmy_domain: example.com\n")
    with pytest.raises(KeyError):
        read_config(str(cfg))

def test_read_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_config('/nonexistent/path/config.yml')


# ---------------------------------------------------------------------------
# check_domain_registrar
# ---------------------------------------------------------------------------

HEADERS = {'X-TCpanel-Token': 'abc123'}

def _mock_get(json_data):
    response = MagicMock()
    response.json.return_value = json_data
    return response

DOMAIN_LIST = [
    {'name': 'example.com', 'product_info': {'product_status': 'active'}},
    {'name': 'other.com',   'product_info': {'product_status': 'active'}},
]

def test_check_domain_registrar_found():
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get(DOMAIN_LIST)):
        result = check_domain_registrar('example.com', HEADERS)
    assert 'example.com' in result
    assert '☑' in result

def test_check_domain_registrar_not_found():
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get(DOMAIN_LIST)):
        result = check_domain_registrar('missing.com', HEADERS)
    assert '☒' in result

def test_check_domain_registrar_inactive_domain():
    domains = [{'name': 'example.com', 'product_info': {'product_status': 'inactive'}}]
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get(domains)):
        result = check_domain_registrar('example.com', HEADERS)
    assert '☒' in result

def test_check_domain_registrar_empty_list():
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get([])):
        result = check_domain_registrar('example.com', HEADERS)
    assert '☒' in result


# ---------------------------------------------------------------------------
# obtain_subdomain_id
# ---------------------------------------------------------------------------

RECORDS = [
    {'id': 42, 'name': 'home', 'type': 'A',   'content': '1.2.3.4'},
    {'id': 99, 'name': 'mail', 'type': 'MX',  'content': 'mail.example.com'},
]

def test_obtain_subdomain_id_found():
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get(RECORDS)):
        result = obtain_subdomain_id('home', HEADERS, '1')
    assert result == [42, '1.2.3.4']

def test_obtain_subdomain_id_not_found():
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get(RECORDS)):
        result = obtain_subdomain_id('ftp', HEADERS, '1')
    assert result == [None, None]

def test_obtain_subdomain_id_wrong_type():
    # 'mail' exists but is MX, not A
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get(RECORDS)):
        result = obtain_subdomain_id('mail', HEADERS, '1')
    assert result == [None, None]

def test_obtain_subdomain_id_empty():
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=_mock_get([])):
        result = obtain_subdomain_id('home', HEADERS, '1')
    assert result == [None, None]


# ---------------------------------------------------------------------------
# obtain_domain_id
# ---------------------------------------------------------------------------

DOMAINS = [
    {'id': 7, 'name': 'example.com'},
    {'id': 8, 'name': 'other.com'},
]

def test_obtain_domain_id_found():
    subdomain_response = _mock_get(RECORDS)
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=subdomain_response):
        result = obtain_domain_id('home', 'example.com', HEADERS, DOMAINS)
    assert result['domain_id'] == '7'
    assert result['subdomain_id'] == 42
    assert result['subdomain_ip'] == '1.2.3.4'

def test_obtain_domain_id_domain_not_found():
    result = obtain_domain_id('home', 'missing.com', HEADERS, DOMAINS)
    assert result == {'domain_id': None, 'subdomain_id': None, 'subdomain_ip': None}

def test_obtain_domain_id_subdomain_not_found():
    subdomain_response = _mock_get([])
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=subdomain_response):
        result = obtain_domain_id('home', 'example.com', HEADERS, DOMAINS)
    assert result['domain_id'] == '7'
    assert result['subdomain_id'] is None
    assert result['subdomain_ip'] is None


# ---------------------------------------------------------------------------
# obtain_my_ip
# ---------------------------------------------------------------------------

def test_obtain_my_ip():
    mock_response = MagicMock()
    mock_response.json.return_value = {'ip': '9.8.7.6'}
    with patch('neodigit_dyndns.dyndns.requests.get', return_value=mock_response):
        ip = obtain_my_ip()
    assert ip == '9.8.7.6'


# ---------------------------------------------------------------------------
# update_ip
# ---------------------------------------------------------------------------

DOMAIN_INFO = {'domain_id': '7', 'subdomain_id': '42', 'subdomain_ip': '1.2.3.4'}

def test_update_ip_calls_put():
    mock_put = MagicMock()
    with patch('neodigit_dyndns.dyndns.requests.put', return_value=mock_put) as mock:
        update_ip(HEADERS, DOMAIN_INFO, '5.6.7.8')
    mock.assert_called_once()
    call_kwargs = mock.call_args
    assert '/dns/zones/7/records/42' in call_kwargs[0][0]

def test_update_ip_sends_correct_content():
    with patch('neodigit_dyndns.dyndns.requests.put') as mock_put:
        update_ip(HEADERS, DOMAIN_INFO, '5.6.7.8')
    _, kwargs = mock_put.call_args
    sent_data = json.loads(kwargs['data'])
    assert sent_data['record']['content'] == '5.6.7.8'

def test_update_ip_includes_content_type():
    with patch('neodigit_dyndns.dyndns.requests.put') as mock_put:
        update_ip(HEADERS, DOMAIN_INFO, '5.6.7.8')
    _, kwargs = mock_put.call_args
    assert kwargs['headers']['Content-Type'] == 'application/json'
    # Original token header must still be present
    assert kwargs['headers']['X-TCpanel-Token'] == 'abc123'


# ---------------------------------------------------------------------------
# create_registry
# ---------------------------------------------------------------------------

def test_create_registry_calls_post():
    with patch('neodigit_dyndns.dyndns.requests.post') as mock_post:
        create_registry('home', HEADERS, DOMAIN_INFO, '5.6.7.8')
    mock_post.assert_called_once()
    url = mock_post.call_args[0][0]
    assert '/dns/zones/7/records' in url

def test_create_registry_sends_correct_payload():
    with patch('neodigit_dyndns.dyndns.requests.post') as mock_post:
        create_registry('home', HEADERS, DOMAIN_INFO, '5.6.7.8')
    _, kwargs = mock_post.call_args
    sent = json.loads(kwargs['data'])
    assert sent['record']['name'] == 'home'
    assert sent['record']['type'] == 'A'
    assert sent['record']['content'] == '5.6.7.8'
    assert sent['record']['ttl'] == 60

def test_create_registry_includes_content_type():
    with patch('neodigit_dyndns.dyndns.requests.post') as mock_post:
        create_registry('home', HEADERS, DOMAIN_INFO, '5.6.7.8')
    _, kwargs = mock_post.call_args
    assert kwargs['headers']['Content-Type'] == 'application/json'
    assert kwargs['headers']['X-TCpanel-Token'] == 'abc123'
