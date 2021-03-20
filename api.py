#coding=utf-8
import requests
import json
import urllib.request
import datetime

zapros = 1

while zapros==1:
	try:
		api_key ='411f595c4c1467dec55ad9b125d12217'
		group = input()
		url = 'https://petrocol.ru/schedule/'+group+'?json=1&key='+api_key
		response = requests.get(url)
		week=datetime.datetime.today().isoweekday()
		if response.status_code==200:
			if week == 1:
				week="monday"
			elif week == 2:
				week='tuesday'
			elif week == 3:
				week='wednesday'
			elif week == 4:
				week='thursday'
			elif week == 5:
				week='friday'
			elif week == 6:
				week='saturday'
			elif week == 7:
				week='sunday'
			else:
				week='eror'
			response_json = json.loads(response.text)
			result = response_json["schedule"][week]
			print(result)
		else:
			print(f"Request returns code response.status_code")
	except:
			print("No data")
