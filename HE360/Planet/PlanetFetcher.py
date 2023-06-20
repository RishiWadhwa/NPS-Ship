import json
import os
import requests

SUBSCRIPTION_ID = '520ca04e-cef3-4da7-8187-165059a57ff1'

API_KEY = os.environ.get('PL_API_KEY', 'PLAK5b0cbee2793343e8a4ddb988b0404223')
BASIC_AUTH = (API_KEY, '')
BASE_URL = "https://api.planet.com/analytics/"

subscription_results_url = BASE_URL + 'collections/' + SUBSCRIPTION_ID + '/items'
print("Request URL: {}".format(subscription_results_url))

resp = requests.get(subscription_results_url, auth=BASIC_AUTH)
data = ""
if resp.status_code == 200:
	print('Yay, you can access analytic feed results!')
	subscription_results = resp.json()
	data = json.dumps(subscription_results, sort_keys=True, indent=4)
else:
    print('Something is wrong:', resp.content)
 
with open("planetjson.json", "w") as file:
 	file.write(data)