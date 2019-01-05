import os
import sys

import requests
import simplejson
from lxml import html


def get_html_tree(url) -> html.HtmlElement:
    """
    TODO
    :param url:
    :return:
    """
    page = requests.get(url, timeout=5)
    page.raise_for_status()
    html_tree = html.fromstring(page.text)
    return html_tree


def get_audio_url(page_tree) -> str:
    """
    TODO
    :param page_tree:
    :type page_tree: lxml.html.HtmlElement
    :return:
    """
    content_uri = page_tree.xpath('.//meta[@itemprop="contentUrl"]/@content')
    # metas = [i.attrib for i in html_tree.xpath('.//meta') if 'itemprop' in i.attrib and 'content' in i.attrib]
    # content_uri = list(filter(lambda x: re.match(r"^(.+)\.mp3$", x['content']), metas))
    if len(content_uri) != 1:
        raise ValueError("2 URLs found")
    return str(content_uri[0])


def get_audio_trans(page_tree):
    """
    TODO
    :param page_tree:
    :return:
    """
    html_element = page_tree.xpath('.//div[@id="acordeon_trascripcion"]//div[@itemprop="articleBody"]')

    interventions = []

    for index, element in enumerate(html_element[0][:-1]):
        e = element.getchildren()[2].getchildren()
        next_word = html_element[0][index + 1].getchildren()[2].getchildren()[0].get("data-stime")
        node = {}
        node['voice'] = element.getchildren()[0].text
        node['start'] = float(e[0].get("data-stime"))
        node['end'] = float(next_word)
        node['text'] = []

        for i, word in enumerate(e[:-1]):
            word_info = {}
            word_info['text'] = word.text
            word_info['start_time'] = float(word.get("data-stime"))
            word_info['end_time'] = float(e[i + 1].get("data-stime"))
            node['text'].append(word_info)

        word_info = {'text': e[-1].text, 'start_time': float(e[-1].get("data-stime")), 'end_time': float(next_word)}
        node['text'].append(word_info)
        interventions.append(node)

    element = html_element[0][-1]
    e = element.getchildren()[2].getchildren()
    node = {}
    node['voice'] = element.getchildren()[0].text
    node['start'] = float(e[0].get("data-stime"))
    node['end'] = float(e[-1].get("data-stime"))
    node['text'] = []

    for i, word in enumerate(e[:-1]):
        word_info = {}
        word_info['text'] = word.text
        word_info['start_time'] = float(word.get("data-stime"))
        word_info['end_time'] = float(e[i + 1].get("data-stime"))
        node['text'].append(word_info)

    interventions.append(node)

    return interventions


def get_audio_file(audio_url, path):
    extension = audio_url.split('.')[-1]
    r = requests.get(audio_url, timeout=30)
    open(os.path.join(path, 'audio.' + extension), 'wb').write(r.content)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Pase la ruta del json + Ruta de salida")
        exit()
    try:
        base_folder = sys.argv[2]
        if not os.path.isdir(base_folder):
            os.mkdir(base_folder)
        input = simplejson.load(open(sys.argv[1]))
        for program in input:
            path = os.path.join(base_folder, program['name'].replace('/', '-').replace(' ', '_'))
            if not os.path.isdir(path):
                os.mkdir(path)
            print(program)
            # url = 'http://play.cadenaser.com/audio/cadenaser_hoyporhoy_20181123_100000_110000/'
            html_tree = get_html_tree(program['uri'])

            audio_url = get_audio_url(html_tree)
            # get_audio_file(audio_url, path)

            trans = get_audio_trans(html_tree)
            open(os.path.join(path, 'trans.json'), 'wb').write(
                simplejson.dumps(trans, indent=4, ensure_ascii=False).replace("'", '"').encode('utf8'))
            # print(trans)
    except Exception as e:
        print(e)
