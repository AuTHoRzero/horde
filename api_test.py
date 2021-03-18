# -*- coding: utf-8 -*-
import requests
import json
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
url = 'https://petrocol.ru/schedule/39-55?json=1&key=411f595c4c1467dec55ad9b125d12217'
head = {}
response = requests.get(url, head=head)
jprint(response.json())