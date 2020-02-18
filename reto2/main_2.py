from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

hashtag='pubg'
browser = webdriver.Chrome('./chromedriver.exe')
browser.get('https://www.instagram.com/explore/tags/'+hashtag)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Extract links from hashtag page
links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)

print(data)

time.sleep(5) 
Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/3.0);")
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
     if re.match("/p", link.get('href')):
         links.append('https://www.instagram.com'+link.get('href'))

# for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
#     links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')

print(links)