from lxml import etree
import json
from io import StringIO
import csv

with open('data.json', 'r') as fh:
    data = fh.read()

oids = json.loads(data)

parser = etree.HTMLParser()


for idx,oid in enumerate(oids):
    #clean up the HTML and convert to dictionary
    html = oid.pop('fileName')
    if html:
        tree = etree.parse(StringIO(html), parser)
        try:
            rows = tree.findall('.//div[@class="row"]')
            for row in rows:
                field = row.find('div[@class="field"]').text
                value = row.find('div[@class="value"]').text
                oid[field] = value
        except etree.XMLSyntaxError as err:
            print(f"HTML parsing error in oids[{idx}]: {oid['name']}")
            print(err)
    
    #remove the nested mibObjectUniqueInfo dictionary and add to oid dict 
    unique_info = oid.pop('mibObjectUniqueInfo')
    oid.update(**unique_info)


#write csv
keys = set().union(*(d.keys() for d in oids))
# keys = toCSV[0].keys()
with open('data.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(oids)
