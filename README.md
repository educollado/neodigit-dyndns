# neodigit-dyndns

[![PyPI version](https://img.shields.io/pypi/v/neodigit-dyndns)](https://pypi.org/project/neodigit-dyndns/)
[![Python](https://img.shields.io/pypi/pyversions/neodigit-dyndns)](https://pypi.org/project/neodigit-dyndns/)
[![License](https://img.shields.io/github/license/educollado/neodigit-dyndns)](https://github.com/educollado/neodigit-dyndns/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/educollado/neodigit-dyndns)](https://github.com/educollado/neodigit-dyndns/commits/main)
[![Mastodon](https://img.shields.io/mastodon/follow/72314?domain=https%3A%2F%2Fmastodon.social&style=social)](https://mastodon.social/@ecollado)

Cliente de DNS dinámico para dominios gestionados en [Neodigit](https://panel.neodigit.net). Comprueba tu IP pública y actualiza automáticamente el registro A de tu subdominio cuando cambia.

## Inicio rápido

```bash
pip install neodigit-dyndns
neodigit-dyndns config.yaml
```

## Instalación

**Desde PyPI:**

```bash
pip install neodigit-dyndns
```

**Desde el código fuente:**

```bash
git clone https://github.com/educollado/neodigit-dyndns.git
cd neodigit-dyndns
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuración

Obtén tu token en [panel.neodigit.net/api-consumers](https://panel.neodigit.net/api-consumers) y crea un fichero YAML:

```yaml
token: TU_TOKEN_AQUI
my_domain: tudominio.com
my_subdomain: subdominio
```

> [!WARNING]
> No subas este fichero a un repositorio público.

**Ejemplo** — para gestionar `home.midominio.com`:

```yaml
token: RgU3dNWT8P4pIq1QZ4UXXXXXXXXXXXXXXXX
my_domain: midominio.com
my_subdomain: home
```

## Uso

```bash
neodigit-dyndns config.yaml
```

Salida de ejemplo:

```
☑ Your domain midominio.com is registered in Neodigit
☑ Your IP has changed from 1.2.3.4 to 5.6.7.8
```

## Automatización con cron

Para actualizar la IP cada 15 minutos, añade esta línea con `crontab -e`:

```
*/15 * * * * neodigit-dyndns /ruta/a/config.yaml >> /var/log/neodigit-dyndns.log 2>&1
```

## Cómo funciona

En cada ejecución el cliente:

1. Verifica que el dominio esté registrado en Neodigit
2. Obtiene la IP pública actual (via [ipify](https://www.ipify.org/))
3. Si el subdominio no existe → lo crea
4. Si la IP no ha cambiado → no hace nada
5. Si la IP ha cambiado → actualiza el registro A

## Requisitos

- Python 3.8+
- Dominio registrado y gestionado en [Neodigit](https://panel.neodigit.net)
- Token de API de Neodigit

## Licencia

[GPL-3.0](https://github.com/educollado/neodigit-dyndns/blob/main/LICENSE)
