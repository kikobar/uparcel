import requests
import json
from config import *
from push import *
import sys
import base64

def track(track_id):
    url = base_url + "api/merchant/auth/"
    payload = json.dumps({
        "api_key": api_key,
        "secret_key": secret_key,
        "api_platform": "Open",
        "api_mode": "production",
        "domain_info": domain
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode(api_key.encode('ascii')).decode('ascii')
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    bear_token = json.loads(response.text)['data']['access_token']
    url = base_url + "api/merchant/parcel-track-status/"
    payload = json.dumps({
        "tracking_number":[
            track_id
            ],
        "merchant_detail":{
            "access_token": bear_token
            }
        })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    
if __name__ == '__main__':
    track(str(sys.argv[1]))
    
