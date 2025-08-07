import argparse
import os
import sys
import time
import json
import requests
import requests_cache
import db
import util
import sescrape
import http.client
from serpapi import GoogleSearch
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import quote

scraperxbase = "https://api.scraperx.com"

SCRAPERXKEY = os.getenv('SCRAPERXKEY')
SERPAPIKEY = os.getenv('SERPAPIKEY')

def scraperx_google_search(query, page=1):
  endpoint = scraperxbase+"/api/v1/google/search"
  
  headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-api-key': SCRAPERXKEY
  }
  
  payload = {
    "country": "us",
    "keyword": query,
    "language": "en",
    "limit": 100,
    "page": page
  }
  print(endpoint)
  print(payload)
  print(headers)
  res = requests.post(endpoint, headers=headers, json=payload)
  
  if res.from_cache:
    print('using cached result')
  
  if res.ok:
    print('got response')
    data = res.json()
    print(data)
    return data
  else:
    print(res)

def scraperx_similar_web(domain):
  endpoint = scraperxbase + "/api/v1/similarweb/web/"+domain
  headers = {
  'Accept': 'application/json',
  'x-api-key': SCRAPERXKEY
  }
  payload = {}
  print(endpoint)
  print(payload)
  print(headers)
  res = requests.get(endpoint, headers=headers, data=payload)
  if res.from_cache:
    print('using cached result')
  if res.ok:
    print('got response')
    data = res.json()
    print(data)
    return data
  else:
    print(res)

def serpapi_ddg_search(query):
  params = {
  "engine": "duckduckgo",
  "q": query,
  "kl": "us-en",
  "start": 5,
  "api_key": SERPAPIKEY
  }
  
  print(params)
  search = GoogleSearch(params)
  results = search.get_dict()
  return results

def serpapi_bing_search(query):
  params = {
  "engine": "bing",
  "q": query,
  "first": "1",
  "count": "50",
  "api_key": SERPAPIKEY
  }

  print(params)
  search = GoogleSearch(params)
  results = search.get_dict()
  return results

def gather_domain_data(datab, domain):
  data = load_data(datab, domain)
  
  # scraperx - google search "link: [domain]"
  if 'google_backlinks' not in data:
    print('getting google_backlinks data')
    data['google_backlinks'] = scraperx_google_search("link:"+domain)
    time.sleep(1.5)
  else:
    print('google_backlinks already exists')
  
  # scraperx - similarweb[:domain]
  if 'similarweb_data' not in data:
    print('getting similarweb data')
    data['similiarweb_data'] = scraperx_similar_web(domain) 
    time.sleep(1.5)
  else:
    print("similarweb_data already exists")
  
  # serpapi - ddg search "link: [domain]"
  if 'ddg_backlinks' not in data:
    print('getting duckduckgo_backlinks')
    data['ddg_backlinks'] = serpapi_ddg_search('link:'+domain)
    time.sleep(1.5)
  else: 
    print('duckduckgo_backlinks already stored')

  # serpapi - bing search "link: [domain]"
  if 'bing_backlinks' not in data:
    print('getting bing_backlinks')
    data['bing_backlinks'] = serpapi_bing_search('link:'+domain)
    time.sleep(1.5)
  else: 
    print('bing_backlinks already stored')

  #print(data)
  insert_data(datab, domain, data)
  
def insert_data(datab, domain, data):
  insert_data = (domain, json.dumps(data), util.unixtime())
  sql = "REPLACE INTO domain (domain, data, timestamp) VALUES (?, ?, ?)"
  datab.insert_one(sql, insert_data)

def load_data(datab, domain):
  sql = "SELECT * FROM domain WHERE domain = '"+domain+"'"
  row = datab.select_one(sql)
  if row is None: 
    return {}
  #print(row)  
  return json.loads(str(row[2]))

def main():
  requests_cache.install_cache('my_cache', backend='sqlite', expire_after=3600)
  parser = argparse.ArgumentParser(prog="seodata", description="SEO Utility CLI")
  subparsers = parser.add_subparsers(dest='operation', required=True)
  backlink_parser = subparsers.add_parser('backlinks', help='Find backlinks to a domain')
  data_parser = subparsers.add_parser('data', help='Gather data about a domain from a variety of sources')
  db_initializer = subparsers.add_parser('db-init', help='Gather data about a domain from a variety of sources')

  backlink_parser.add_argument('--domain', required=True, help='Domain to find backlinks for')
  backlink_parser.add_argument('--results', type=int, default=10, help='Number of results to fetch (default: 10)')
  backlink_parser.add_argument('--search-engine', default='google', help='Search engine to use (google, duckduckgo, yandex)')

  data_parser.add_argument('--domain', required=True, help='Domain to collect data')

  args = parser.parse_args()
  datab = db.sqliteDB('database.sqlite3')

  if args.operation == 'backlinks':
    try:
      data = perform_backlink_search(args.domain, args.results, args.search_engine)
    except Exception as e:
      print(e)

  elif args.operation == 'data':
    gather_domain_data(datab, args.domain)

  elif args.operation == 'db-init':
    sql = "CREATE TABLE domain (id INTEGER PRIMARY KEY, domain TEXT UNIQUE, data TEXT, timestamp INT)"
    datab.query(sql)
    datab.commit()

  else:
      parser.print_help()
      sys.exit(1)

if __name__ == "__main__":
    main()
