import requests
import xml.etree.ElementTree as etree
from dateutil.parser import parse

url_rss = 'https://www.mlab.im.dendai.ac.jp/bthesis/bachelor/rss.xml'

res = requests.get(
    url_rss,
    auth=(os.environ['TDU_ID'], os.environ['TDU_PASS']),
    timeout=30)
res.encoding = res.apparent_encoding

tree = etree.fromstring(res.text)

for item in [x for x in tree.getiterator() if 'item' in x.tag]:
    for _, v in item.attrib.items():
        print(parse("".join(v.split('?')[1].split(' JST'))))
    for elem in item.getiterator():
        if 'description' in elem.tag:
            print(elem.text)
