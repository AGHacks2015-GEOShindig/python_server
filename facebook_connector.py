# encoding: UTF-8
from slugify import slugify
import requests
import simplejson as json
import sys

from pprint import pprint
from elasticsearch import Elasticsearch
from tqdm import tqdm
ES_CREDENTIALS = {
    'host': 'vps207097.ovh.net',
    'port': 9200
}

es = Elasticsearch([{'host': ES_CREDENTIALS['host'], 'port': ES_CREDENTIALS['port']}])

CITIES = [
'Warszawa', 'Kraków', 'Łódź', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin', 'Bydgoszcz', 
'Lublin', 'Katowice', 'Białystok', 'Gdynia', 'Częstochowa', 'Radom', 'Sosnowiec', 'Toruń', 
'Kielce', 'Rzeszów', 'Gliwice', 'Zabrze', 'Olsztyn', 'Bielsko-Biała', 'Bytom', 'Ruda Śląska', 
'Rybnik', 'Zielona Góra', 'Tychy', 'Gorzów Wielkopolski', 'Dąbrowa Górnicza', 'Elbląg', 
'Płock', 'Opole', 'Wałbrzych', 'Włocławek', 'Tarnów', 'Chorzów', 'Koszalin'
]
CITIES = [slugify(x) for x in CITIES]
URL = "https://graph.facebook.com/v2.5/search?"


for city in CITIES:
	print('Current city: ' + city)

	params = [
	 'q='+city,
	 'city='+city,
	 'country=Poland',
	 'type=event',
	 'fields=name%2C%20start_time%2Cend_time%2Cplace',
	 'limit=99999999',
	 'access_token=CAACEdEose0cBAFWdl51YCKY9skZBLHi8o4FQxi5K7GswiY44nB8mBuWZBETHgg8UPl0Y5IWsYZBPL3on1kDxbTmGHf0rOz6r1HwfxLZBv6NArvvKwBWFceQYJSeZC2JhGaBpLnGJCZBdkMNfkj492GRdwnvBLzqfJNzMsZASKFvn7XwP8ZBRuWhwjP66pi9Vi7H15UZAjRtmu0DZAKZAHte5DZC13GcgY0WMQ94ZD'
	]	

	full_url = URL + '&'.join(params)

	headers = {'Content-type': 'application/json'}
	r = requests.get(full_url, headers=headers)
	events = json.loads(r.text)['data']

	for event in tqdm(events):
		try:
			e = event['place']['location']
			event['place']['location']['geo_cord'] = ','.join([str(e['longitude']), str(e['latitude'])])
		except Exception, e:
			pass
		es.index(
			index='fb_events',
			doc_type='event',
			body=event,
			request_timeout=60
		)