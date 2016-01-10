import requests 
from bs4 import BeautifulSoup
import json
import string
import csv

BASE_URL = 'http://www.property24.co.ke/apartments-flats-to-rent-in-westlands-s14537'

def scrape(params=None, payload=None):
	url = BASE_URL + '/'.join(params) if params else BASE_URL
	if not payload:
		payload = {'ToPrice':'100000', 'FromPrice':'20000', 'PropertyTypes':'apartments-flats,townhouses'}
	r = requests.get(url,payload)
	data = None
	if r.status_code == 200:
		data = r.text.encode('utf-8')
		if data:
			return data
	return None

def parse_html(data):
	if data:
		soup = BeautifulSoup(data)
		divs = soup.find_all('div', class_="propertyTileWrapper")
		return divs

def parse_div(div):
	d = {}
	a = div.find('a', class_='main-link')
	if a:
		d['href'] = a.attrs.get('href',"")
		d['desc'] = clean_text(a.text)
	s = div.find('span','lisitng-cost')
	if s:
		d['price'] = int(clean_text(s.text,remove_punc=True,remove_letters=True))
	p = div.find('p', class_='listing-address')
	if p:
		d['location'] = p.text
	y = div.find('span', attrs={'original-title':'Bedrooms'})
	if y:
		d['bedrooms'] = int(y.text)
	return d