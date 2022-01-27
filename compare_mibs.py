from requests import Session
import json
from lxml import etree
from io import StringIO
import csv

# releases1/2 must match what's available on mib-explorer
product = "Junos+OS"
release2 = "14.1x53-D49"
release1 = "18.4R3"


compare_url = "https://apps.juniper.net/mib-explorer/compareReleases.html"
headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}

# Setup session
session = Session()
session.headers.update(headers)

#Access compare page to retrieve set-cookies
session.get("https://apps.juniper.net/mib-explorer/compare.jsp")


# Enumerate paged responses
page = 0
body = f"product={product}&release1={release1}&release2={release2}&withDesc=true"
oids = []
while True:
    print(body + f"&pgNo={page}")
    r = session.post(compare_url, data=body + f"&pgNo={page}")
    if r.status_code == 200:
        diff = json.loads(r.text)
        if len(diff['list']) > 0:
            oids += diff['list']
            page += 1
        else:
            print("Last page!")
            break
 
    else:
        print("Last page!")
        break

print(f"Found {len(oids)} OIDs different between {release1} and {release2}.")


info_url = "https://apps.juniper.net/mib-explorer/getObjectDetails.html"

body = f"product={product}&release={release1}"

for oid in oids:
    print(body + f"&objectName={oid.get('name')}")
    r = session.post(info_url, data=body + f"&objectName={oid.get('name')}")
    oid.update(r.json()[0])


#write data out for use with parse_xml.py
with open("data.json", "w") as fh:
    fh.write(json.dumps(oids))

new_traps = [oid for oid in oids if "TRAP" in oid['fileName']]
with open("new_traps.txt", "w") as fh:
    fh.write(json.dumps(new_traps))