import requests
import json
from config import *
from push import *
import sys
import base64

def req_delivery():
    order_id = int(input('Enter the Order ID: ') or '1')
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
    url = base_url + "api/merchant/delivery-type-service-list/"
    payload = json.dumps({
        "access_token": bear_token
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    delivery_type_list = json.loads(response.text)['data']['delivery_type']
    for key in delivery_type_list:
        delivery_type_json = json.dumps(key)
        delivery_type_json = json.loads(delivery_type_json)
        print("["+str(delivery_type_json['id_delivery_type'])+"] - "+delivery_type_json['delivery_type'])
    delivery_type = int(input('Enter delivery type ['+str(default_delivery_type)+']: ') or default_delivery_type)
    quantity = int(input('Enter number of packets [1]: ') or '1')
    weight = str(input('Enter weight in kg ['+str(default_weight)+']: ') or default_weight)
    length = str(input('Enter length in cm ['+str(default_length)+']: ') or default_length)
    width = str(input('Enter width in cm ['+str(default_width)+']: ') or default_width)
    height = str(input('Enter height in cm ['+str(default_height)+']: ') or default_height)
    print('Enter pickup details')
    pickup_name = str(input("Enter sender's name ["+default_sender+"]: ") or default_sender)
    pickup_contact_number = str(input("Enter sender's contact number ["+default_sender_number+"]: ") or default_sender_number)
    pickup_address = str(input('Enter pickup address ['+default_pickup_address+']: ') or default_pickup_address)
    pickup_pincode = str(input('Enter pickup postal code ['+default_pickup_pincode+']: ') or default_pickup_pincode)
    pickup_remark = str(input('Enter pickup remarks ['+default_pickup_remark+']: ') or default_pickup_remark)
    print('Enter delivery details')
    delivery_name = str(input("Enter receiver's name ["+default_delivery_name+"]: ") or default_delivery_name)
    delivery_contact_number = str(input("Enter receiver's number ["+default_delivery_number+"]: ") or default_delivery_number)
    delivery_email = str(input("Enter receiver's email ["+default_delivery_email+"]: ") or default_delivery_email)
    delivery_address = str(input("Enter delivery address ["+default_delivery_address+"]: ") or default_delivery_address)
    delivery_pincode = str(input("Enter delivery postal code ["+default_delivery_pincode+"]: ") or default_delivery_pincode)
    delivery_remark = str(input('Enter delivery remarks ['+default_delivery_remark+']: ') or default_delivery_remark)
    print()
    print('From:')
    print(pickup_name)
    print(pickup_address)
    print(pickup_pincode)
    print('Contact: '+pickup_contact_number)
    print('Remarks: '+pickup_remark)
    print()
    print('To:')
    print(delivery_name)
    print(delivery_address)
    print(delivery_pincode)
    print('Contact: '+delivery_contact_number)
    print('Remarks: '+delivery_remark)
    print()
    print('Delivery type: '+str(delivery_type))
    print()
    confirm = str(input('Confirm Y/N? [N]: ') or 'N')
    if confirm != 'y' and confirm !='Y':
        print('You have canceled your request')
        return
    
    url = base_url + "api/merchant/order-submit/"
    payload = json.dumps({
        "merchant_detail":{
            "access_token": bear_token
            },
        "delivery_package":[{
            "quantity": quantity,
            "weight":{
                "value": weight,
                "units": "kg"
                },
            "dimensions":{
                "length": length,
                "width": width,
                "height": height,
                "units": "cm"
                }
            }],
        "order_id": order_id,
        "pickup_detail":{
            "name": pickup_name,
            "contact_number": pickup_contact_number,
            "pickup_address": pickup_address,
            "pickup_pincode": pickup_pincode,
            "pickup_remark": pickup_remark,
            "vehicle_type": default_vehicle
            },
        "customer_detail":{
            "name": delivery_name,
            "email": delivery_email,
            "contact_number": delivery_contact_number,
            "delivery_address": delivery_address,
            "delivery_pincode": delivery_pincode,
            "delivery_type": delivery_type,
            "delivery_remark": delivery_remark,
            "api_response_url": web_hook
            }
        })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    push(json.loads(json.dumps({
        "order_id": order_id,
        "data": json.loads(response.text)
        })))
    
if __name__ == '__main__':
    req_delivery()
    
