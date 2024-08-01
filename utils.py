import json
import browser_cookie3
from constants import *


config_params = ['BROWSER', 'SERVER_UTC', 'DELAY_MINUTE', 'RANDOMIZE', 'RANDOM_RANGE',
                 'ACT_ID', 'DOMAIN_NAME', 'SCHEDULER_NAME']


def init_environment() -> dict:
    try:
        config = json.load(open(os.path.join(APP_PATH, 'config.json'), 'r'))
        for param in config_params:
            if param not in config:
                raise Exception(f"ERROR: Broken config file, {param} not found")
    except Exception as e:
        print(repr(e))
        print("Config not found/corrupted! Making default config...")
        config = {
            'BROWSER': 'all',
            'SERVER_UTC': 8,
            'DELAY_MINUTE': 0,
            'RANDOMIZE': False,
            'RANDOM_RANGE': 3600,
            'ACT_ID': 'e202102251931481',
            'DOMAIN_NAME': '.hoyolab.com',
            'SCHEDULER_NAME': 'HoyolabCheckInBot'
        }
        config_file = open(os.path.join(APP_PATH, 'config.json'), 'w')
        config_file.write(json.dumps(config, indent=4))
    return config


def get_cookies(config: dict):
    try:
        if config['BROWSER'].lower() == 'all':
            cookies = browser_cookie3.load(domain_name=config['DOMAIN_NAME'])
        elif config['BROWSER'].lower() == 'firefox':
            cookies = browser_cookie3.firefox(domain_name=config['DOMAIN_NAME'])
        elif config['BROWSER'].lower() == 'chrome':
            cookies = browser_cookie3.chrome(domain_name=config['DOMAIN_NAME'])
        elif config['BROWSER'].lower() == 'opera':
            cookies = browser_cookie3.opera(domain_name=config['DOMAIN_NAME'])
        elif config['BROWSER'].lower() == 'edge':
            cookies = browser_cookie3.edge(domain_name=config['DOMAIN_NAME'])
        elif config['BROWSER'].lower() == 'chromium':
            cookies = browser_cookie3.chromium(domain_name=config['DOMAIN_NAME'])
        else:
            raise Exception("ERROR: Supported browser not defined in config.json")
    except Exception as e:
        print(f"{e}\n Supported browsers: {SUPPORTED_BROWSERS}")
        return None
    try:
        for cookie in cookies:
            if cookie.name == "cookie_token":
                break
        else:
            raise Exception("ERROR: Need to login before using the bot")
    except Exception as e:
        print(
            f'{e}\n'
            f"Login information not found!"
            f" Please login first to hoyolab(https://www.hoyolab.com/genshin/) before using the bot."
        )
        return None
    return cookies
