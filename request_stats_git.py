import requests
import time
import random

session = requests.Session()
url = 'https://visitor-badge.glitch.me/badge'

while (True):
    r = session.get(url, params={'page_id': 'damminhtien'})
    print(str(r.content))
    time.sleep(random.randint(1, 5))
