import requests
import time
from time import sleep
from time import time as getcurrtimestamp
import json
etag = None


def timeprint(text):
    print(time.strftime(f'%D - %T {text}'))

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Raspbian Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36'}
uff = 'https://storage.googleapis.com/tdc-app-emea-prod.appspot.com/v0/a/defta.json'
while True:
    if etag:
        headers.update({'If-None-Match':etag})
    r = requests.get(uff, headers = headers)
    if r.status_code == 200:
        timeprint('Still no new episode...')
        etag = r.headers['ETag']
        timest = getcurrtimestamp()
        with open(f'defta-{timest}.json', 'w',encoding = 'utf-8-sig') as f:
            f.write(json.dumps(r.json(), indent = 4))
        if not '"Folge 213"' in r.text:
            o = r.json()
            time_str = o['cache_time']
            
            print('Sleeping 60 seconds...', time_str)
            sleep(60)
        else:
            break
    elif r.status_code == 304:
        timeprint('Nothing changed')
        sleep(1)
    else:
        timeprint(f'Recieved unexpected status code {r.status_code}'),