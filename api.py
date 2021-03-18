import requests

answer = requests.get('https://petrocol.ru/schedule/39-55?json=1&key=411f595c4c1467dec55ad9b125d12217').json()
print (answer)