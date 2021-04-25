import requests
from requests_ntlm2 import HttpNtlmAuth

f = open('/home/author/horde/test.txt','w')

auth = HttpNtlmAuth('10190128', 'nhPpYu90Ag')
url = 'https://portal.petrocollege.ru/Lists/List/DispForm.aspx?ID=2648&ContentTypeId=0x0100FCE36C921937184B9D60D386C7DF6753'
r = requests.get(url, auth=auth)

f.write(r.text)