import requests

from utils import *
from constants import *
import browser_cookie3


config = init_environment()
cookies = get_cookies(config)
if cookies is None:
    exit()


def getDailyStatus():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': f'https://act.hoyolab.com/',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('lang', 'en-us'),
        ('act_id', config['ACT_ID']),
    )
    url = f'https://sg-hk4e-api.hoyolab.com/event/sol/sign'
    try:
        response = requests.post(url, headers=headers, params=params, cookies=cookies)
        response = response.json()
        if response['retcode'] == 0:
            return True, "Daily reward claimed!"
        elif response['retcode'] == -5003:
            return True, "Daily reward had been already claimed."
        elif response['retcode'] == -100:
            return False, "Not logged in."
        else:
            return False, f"Unknown error, retcode: {response['retcode']}"
    except requests.exceptions.ConnectionError as e:
        print("CONNECTION ERROR: cannot get daily check-in status")
        print(e)
        return None


print(getDailyStatus())
