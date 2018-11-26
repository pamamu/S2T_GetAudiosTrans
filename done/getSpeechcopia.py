import requests
from lxml import html
import sys
import requests

if len(sys.argv) != 2:
    print("Pase la URL del programa como argumento")
    exit()
page = requests.get(sys.argv[1])
tree = html.fromstring(page.text)
html_element = tree.xpath('.//pre')
print(len(html_element[0]))
