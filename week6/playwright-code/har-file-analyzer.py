import json
import pprint
from urllib.parse import urlparse

with open("test.har", "r") as f:
    data = json.load(f)

entries = data["log"]["entries"]
request_urls = set()

for entry in entries:
    request_url = entry["request"]["url"]
    parsed = urlparse(request_url)
    request_urls.add(f"{parsed.scheme}://{parsed.netloc}")


pprint.pprint(request_urls)
