import csv
import requests
import json

countries_details = []

with open('countries.csv', 'rt') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        countries_details.append(row)

ofile  = open('countries_output.csv', "wt")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)



headers = {
	'authority' : 'maps.googleapis.com',
	'method': 'GET',
	'path': '/maps/api/place/autocomplete/json',
	'scheme': 'https',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'accept-encoding': 'gzip, deflate, sdch, br',
	'accept-language': 'en-US,en;q=0.8',
	'cache-control':'max-age=0',
	'upgrade-insecure-requests': '1',
	'content-length': '56',
	'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'x-client-data': 'CJe2yQEIo7bJAQjBtskBCKmdygE=',
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
}

url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json';

for country_details in countries_details:
	country_name = country_details[1]
	r = requests.get('https://maps.googleapis.com/maps/api/place/autocomplete/json?input='+country_name+'&types=(regions)&key=AIzaSyClDJ30upVkHyCP8IMT5ayCu_3rSu2ag7E')
	data = json.loads(r.text)

	if data['predictions'] == 'OK' and len(data['predictions']) and len(data['predictions'][0]) and len(data['predictions'][0]['types']) and data['predictions'][0]['types'][0] == 'country':
		print('entering place_id for '+country_name)
		writer.writerow([data['predictions'][0]['place_id'], country_details[1], country_details[0]])
	else:
		writer.writerow(["sparshith", country_details[1], country_details[0]])

print("Finishem")
ofile.close()	