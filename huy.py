import requests
from requests_ntlm2 import HttpNtlmAuth
from AdvancedHTMLParser import AdvancedHTMLParser


USERNAME = '10190128'
PASSWORD = 'nhPpYu90Ag'

    
def auth(s, username, password):
    auth = HttpNtlmAuth(username, password)
    s.auth = auth
    result = s.get('https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
    

def get_form_digest(s):
    body = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">  <soap:Body>    <GetUpdatedFormDigest xmlns="http://schemas.microsoft.com/sharepoint/soap/" />  </soap:Body></soap:Envelope>'
    headers = s.headers.copy()
    headers['SOAPAction'] = 'http://schemas.microsoft.com/sharepoint/soap/GetUpdatedFormDigest'
    headers['Content-Type'] =  'text/xml'
    result = s.post('https://portal.petrocollege.ru/_vti_bin/sites.asmx', data=body, headers=headers).text
    digest = result.split('GetUpdatedFormDigestResult>')[1].split('<')[0]
    return digest    

#filter = ['group', 'teacher', 'aud']
#param 0=all or option values
#action if param==0 then selectaction else kriteria
def get_params(page, s, filter, param, action):
    params = {
        'ctl00$ScriptManager': 'ctl00$ctl47$g_463119f4_303b_4073_861b_b8e973140866$UpdatePanel1|ctl00$ctl47$g_463119f4_303b_4073_861b_b8e973140866$selectaction',
        'ctl00$ctl47$g_463119f4_303b_4073_861b_b8e973140866$selectaction': filter,
        'ctl00$ctl47$g_463119f4_303b_4073_861b_b8e973140866$kriteria': param,
        #'ctl00$ctl47$g_d125daf0_6a1f_48af_b036_28c62a39b066$selectaction': '0',
        #'ctl00$ctl47$g_d125daf0_6a1f_48af_b036_28c62a39b066$kriteria': '------',
        '__EVENTTARGET': 'ctl00$ctl47$g_463119f4_303b_4073_861b_b8e973140866$' + action,
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        '__EVENTVALIDATION': '',
        '__REQUESTDIGEST': ''
    }
    if '<!DOCTYPE html >' in page:
        params['__VIEWSTATE'] = page.split('__VIEWSTATE" value="')[1].split('"')[0]
        params['__VIEWSTATEGENERATOR'] = page.split('__VIEWSTATEGENERATOR" value="')[1].split('"')[0]
        params['__EVENTVALIDATION'] = page.split('__EVENTVALIDATION" value="')[1].split('"')[0]
        params['__REQUESTDIGEST'] = page.split('__REQUESTDIGEST" value="')[1].split('"')[0]
    else:
        for line in page.split('\n'):
            if '__EVENTTARGET' in line:
                params['__VIEWSTATE'] = line.split('__VIEWSTATE|')[1].split('|')[0]
                params['__VIEWSTATEGENERATOR'] = line.split('__VIEWSTATEGENERATOR|')[1].split('|')[0]
                params['__EVENTVALIDATION'] = line.split('__EVENTVALIDATION|')[1].split('|')[0]
                params['__REQUESTDIGEST'] = get_form_digest(s)
                break
    
    return params
            
def get_groups(s):
    page = s.get('https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx').text
    params = get_params(page, s, 'aud', '0', 'selectaction')
    headers = s.headers.copy()
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['X-MicrosoftAjax'] = 'Delta=true'
    headers['Referer'] = 'https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx'
    headers['Origin'] = 'https://portal.petrocollege.ru'
    headers['Accept'] = '*/*'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Accept-Language'] = 'en-US,en;q=0.9'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    s.cookies.update({
        'databaseBtnText': '0',
        'databaseBtnDesc': '0',
        'WSS_FullScreenMode': 'false'
        })
    result = s.post('https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx', data=params, headers=headers).text

   
def main():
    s = requests.session()
    s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    s.proxies = {'https': 'http://127.0.0.1:8888'}
    s.verify = False
    auth(s, USERNAME, PASSWORD)
    group = get_groups(s)
    
 
if __name__ == '__main__':
    main()

