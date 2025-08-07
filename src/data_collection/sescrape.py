import os
import sys
import time
import json
import requests
import requests_cache
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import quote

def perform_backlink_search(domain, results, search_engine):
  search_engine = search_engine.lower()
  if search_engine == "google":
    return get_serpapi_results(domain, results)
  elif search_engine == "duckduckgo":
    return scrape_duckduckgo(domain, results)
  elif search_engine == "yandex":
    return scrape_yandex(domain, results)
  else:
    raise ValueError(f"Unsupported search engine: {search_engine}")

def get_serpapi_results(domain, results):
  api_key = os.getenv("SERPAPI_API_KEY")
  if not api_key:
      raise EnvironmentError("Missing SERPAPI_API_KEY environment variable.")

  params = {
    "engine": "google",
    "q": f"link:{domain}",
    "num": results,
    "api_key": api_key
  }

  res = requests.get("https://serpapi.com/search", params=params)
  data = res.json()
  results = []

  for r in data.get("organic_results", []):
    results.append({
      "url": r.get("link"),
      "title": r.get("title"),
      "snippet": r.get("snippet", "")
    })
  return results

def scrape_duckduckgo(domain, results):
  headers = {
    "User-Agent": "Mozilla/5.0"
  }
  query = f"link: {domain}"
  search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
  links = []
  seen = set()

  while len(links) < results:
    print(f"Fetching DuckDuckGo: {search_url}", file=sys.stderr)
    res = requests.post(search_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    for item in soup.find_all('div', class_="result"):
      h2 = item.find('h2', class_="result__title")
      anchor = h2.find('a')
      result_title = anchor.get_text(strip=True)
      result_url = anchor.get('href')
      snippet = item.find('a', class_="result__snippet")
      result_snippet = snippet.get_text(strip=True)
      print(item)
      if result_url not in seen:
        links.append({
          "url": result_url,
          "title": result_title,
          "snippet": result_snippet,
        })
        
        seen.add(result_url)
        if len(links) >= results:
          break
      
    next_form = soup.select_one("form", {"name": "nextForm"})
    print("so far:")
    print(links)
    if not next_form:
      print("that was the last page")
      break  # no more pages

    print("another page!")
    search_url = "https://html.duckduckgo.com" + next_form['action']
    time.sleep(1)
  return links

def scrape_yandex(domain, results):
  headers = {
    "User-Agent": "Mozilla/5.0"
  }
  query = f"link:{domain}"
  search_url = f"https://yandex.com/search/?text={quote(query)}"
  links = []
  page = 0

  while len(links) < results:
    url = f"{search_url}&p={page}"
    print(f"Fetching Yandex: {url}", file=sys.stderr)
    res = requests.get(url, headers=headers)
    print("from cache?")
    print(res.from_cache)  # True or False
    #exit(0)
    #print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup)
    items = soup.select('.organic__url-container')

    for item in items:
      print(item)
      link_tag = item.select_one('a')
      title_tag = item.find_previous('h2')
      if link_tag and title_tag:
        print(link_tag)
        print(title_tag)
        url = link_tag['href']
        title = title_tag.text.strip()
        links.append({
          "url": url,
          "title": title,
          "snippet": ""
        })
        if len(links) >= results:
          break

    page += 1
    time.sleep(1)

    return links
