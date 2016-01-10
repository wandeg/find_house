import requests 
from bs4 import BeautifulSoup
import json
import string
import csv

BASE_URL = 'http://www.lamudi.co.ke/'

def scrape(params=None, payload=None):
	url = BASE_URL + '/'.join(params) if params else BASE_URL
	if not payload:
		payload = {'page':'1'}
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
		divs = soup.find_all('div', class_="listing-info")
		return divs

def scrape_all(loop=True):
	params = ['apartment','for-rent','price:20000-100000']
	curr_page = 1
	data = scrape(params)
	info = []
	if data:
		valid = parse_html(data)
		if valid and len(valid):
			info.extend(valid)
			if loop:
				while valid and len(valid):
					curr_page+=1
					payload={'page':str(curr_page)}
					data = scrape(params,payload)
					valid = parse_html(data)
					if valid and len(valid):
						info.extend(valid)
	return info

def clean_text(text,remove_punc=False, remove_letters=False):
	text = str(text.replace('  ',"").strip('\n'))
	if remove_punc:
		text = text.translate(string.maketrans("",""),string.punctuation)
	if remove_letters:
		text = text.translate(string.maketrans("",""),string.letters)
	return text

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



