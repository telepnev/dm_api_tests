"""
10af8997-6b3a-41b5-a975-c514b320f063

curl -X 'PUT' \
  'http://185.185.143.231:5051/v1/account/10af8997-6b3a-41b5-a975-c514b320f063' \
  -H 'accept: text/plain'


"""
import pprint

import requests

# url = "http://185.185.143.231:5051/v1/account"
# headers = {
#     "Content-Type": "application/json",
#     "Accept": "*/*"
# }
# data = {
#     "login": "tel_01",
#     "email": "tel_01@mail.vu",
#     "password": "12345678"
# }
#
# response = requests.post(url, headers=headers, json=data)

# print(response.status_code)
# pprint.pprint(response.json())


# ====== Activation token

TOKEN = "10af8997-6b3a-41b5-a975-c514b320f063"

url = f"http://185.185.143.231:5051/v1/account/{TOKEN}"
headers = {
    "Accept": "*/*"
}

response = requests.put(url, headers=headers)

print(response.status_code)
pprint.pprint(response.json())

response_json = response.json()
print(response_json['resource']['rating']['quantity'])
