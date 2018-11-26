import requests
from lxml import html
import sys

# if len(sys.argv) != 2:
#     print("Pase la URL del programa como argumento")
#     exit()
page = requests.get('http://play.cadenaser.com/audio/cadenaser_hoyporhoy_20181123_100000_110000/')
tree = html.fromstring(page.text)
html_element = tree.xpath('.//div[@id="acordeon_trascripcion"]//div[@itemprop="articleBody"]')

interventions = []

for element in html_element[0]:
        e = element.getchildren()[2].getchildren()
        node = {}
        node['voice'] = element.getchildren()[0].text
        node['start'] = float(e[0].get("data-stime"))
        node['end'] = float(e[len(e)-1].get("data-stime"))
        interventions.append(node)

print(interventions)
