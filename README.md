# Dynamic DNS with Neodigit's API

![GitHub](https://img.shields.io/github/license/educollado/neodigit-dyndns)
![GitHub last commit](https://img.shields.io/github/last-commit/educollado/neodigit-dyndns)
![GitHub repo size](https://img.shields.io/github/repo-size/educollado/neodigit-dyndns)
![Twitter Follow](https://img.shields.io/twitter/follow/ecollado)
![Mastodon Follow](https://img.shields.io/mastodon/follow/72314?domain=https%3A%2F%2Fmastodon.social&style=social)

Cliente de DNS dinámico para dominios gestionados en [Neodigit](https://panel.neodigit.net). Comprueba tu IP pública y actualiza automáticamente el registro A de tu subdominio.

## Links

* GitHub: https://github.com/educollado/neodigit-dyndns
* PyPI: https://pypi.org/project/neodigit-dyndns/
* API Neodigit: https://developers.neodigit.net/

## Instalación

**Desde PyPI:**

```bash
pip install neodigit-dyndns
```

**Desde el código fuente con venv:**

```bash
git clone https://github.com/educollado/neodigit-dyndns.git
cd neodigit-dyndns
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Configuración

Crea un fichero YAML (por ejemplo `config.yaml`) con las siguientes claves:

```yaml
token: TU_TOKEN_AQUI
my_domain: tudominio.com
my_subdomain: subdominio
```

Puedes obtener tu token en: https://panel.neodigit.net/api-consumers

**Ejemplo:** para actualizar `home.midominio.com`:

```yaml
token: RgU3dNWT8P4pIq1QZ4UXXXXXXXXXXXXXXXX
my_domain: midominio.com
my_subdomain: home
```

> **Importante:** no compartas ni subas este fichero a un repositorio público.

## Uso

```bash
python -m neodigit_dyndns config.yaml
```

O si lo instalaste via pip:

```bash
neodigit-dyndns config.yaml
```

## Automatización con cron

Para actualizar la IP cada 15 minutos, añade esta línea a tu crontab (`crontab -e`):

```bash
*/15 * * * * neodigit-dyndns /ruta/a/config.yaml >> /var/log/neodigit-dyndns.log 2>&1
```

## Comportamiento

El cliente realiza las siguientes comprobaciones en cada ejecución:

1. Verifica que el dominio esté registrado en Neodigit
2. Obtiene la IP pública actual
3. Si el subdominio no existe → lo crea
4. Si el subdominio ya existe y la IP no ha cambiado → no hace nada
5. Si la IP ha cambiado → actualiza el registro A

## Licencia

[GPL-3.0](https://github.com/educollado/neodigit-dyndns/blob/main/LICENSE)
