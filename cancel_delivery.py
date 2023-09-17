import requests
import json
from config import *
from push import *
import sys
import base64

def cancel_delivery(order_id):
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
    url = base_url + "api/merchant/order-cancel/"
    payload = json.dumps({
        "merchant_detail":{
            "access_token": bear_token
            },
        "order_id": order_id
        })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    push(json.loads(json.dumps({
        "order_id": order_id,
        "data": json.loads(response.text)
        })))
    
if __name__ == '__main__':
    cancel_delivery(str(sys.argv[1]))
    
