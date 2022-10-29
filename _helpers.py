import requests

from datetime import datetime
from pathlib import Path


def parse_bool_value(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {'true', 'yes', '1'}
    else:
        raise ValueError(f'expected bool or string; got {type(value)}')


def get_swagger_config():
    return {
        'title': 'Pixoo REST',
        'version': Path('version.txt').read_text(),
        'description': 'A RESTful API to easily interact with the Wi-Fi enabled {} devices.'.format(
            '<a href="https://www.divoom.com/de/products/pixoo-64">Divoom Pixoo</a>'
        ),
        'termsOfService': ''
    }


def try_to_request(url):
    try:
        print(f'[ {datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")} ] Trying to request "{url}" ... ', end='')

        if requests.get(url).status_code == 200:
            print('OK.')
            return True
    except:
        print('FAILED.')
        return False
