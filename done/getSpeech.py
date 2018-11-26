import requests
from lxml import html
import sys
import requests
from multiprocessing import Pool, cpu_count

def process(url, element, i):
    r = requests.get(url + element, stream=True)
    with open('speech_audios/' + element, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return url + element, i

def complete(arg):
    print(arg)


if len(sys.argv) != 2:
    print("Pase la URL del programa como argumento")
    exit()
page = requests.get(sys.argv[1])
tree = html.fromstring(page.text)
html_element = tree.xpath('.//pre')

pool = Pool(processes=cpu_count())
for i in range(6928,len(html_element[0])):
    element = html_element[0][i].get("href")
    if element != None:
        pool.apply_async(func=process, args=(sys.argv[1],element,i, ), callback=complete)
pool.close()
pool.join()

