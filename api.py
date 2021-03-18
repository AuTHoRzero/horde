import requests
import json

def jprint(obj):
	page = json.dumps(obj,sort_keys=True,indent=4)
	print(page)

response = requests.get('https://petrocol.ru/schedule/39-55?json=1&key=411f595c4c1467dec55ad9b125d12217')
jprint(response.json())
