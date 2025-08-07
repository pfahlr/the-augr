import re
import hashlib
from datetime import datetime

headers = {
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"accept-encoding":"gzip, deflate, br, zstd",
"accept-language":"en-US,en;q=0.9",
"cache-control":"max-age=0",
"dnt":"1",
"priority":"u=0, i",
"sec-ch-ua":'"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
"sec-ch-ua-mobile":"?0",
"sec-ch-ua-platform":"Linux",
"sec-fetch-dest":"document",
"sec-fetch-mode":"navigate",
"sec-fetch-site":"same-origin",
"sec-fetch-user":"?1",
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

def hash(data):
  hash_object = hashlib.sha256(data.encode('utf-8'))
  full_hash_value = int(hash_object.hexdigest(), 16)
  return full_hash_value

def unixtime():
  current_datetime = datetime.now()
  # Convert the datetime object to a Unix timestamp (seconds since the epoch)
  timestamp = current_datetime.timestamp()
  return timestamp
