import os
import socket

import simplejson

import requests
from lxml import html


def get_html_tree(url) -> html.HtmlElement:
    """
    TODO DOCUMENTATION
    :param url:
    :return:
    """
    page = requests.get(url, timeout=30)
    page.raise_for_status()
    html_tree = html.fromstring(page.text)
    return html_tree


def get_audio_url(page_tree) -> str:
    """
    TODO DOCUMENTATION
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
    TODO DOCUMENTATION
    :param page_tree:
    :return:
    """
    html_element = page_tree.xpath('.//div[@id="acordeon_trascripcion"]//div[@itemprop="articleBody"]')

    interventions = []

    for index, element in enumerate(html_element[0][:-1]):
        e = element.getchildren()[2].getchildren()
        next_word = html_element[0][index + 1].getchildren()[2].getchildren()[0].get("data-stime")
        node = {'voice': element.getchildren()[0].text,
                'start': float(e[0].get("data-stime")),
                'end': float(next_word),
                'text': []}

        for i, word in enumerate(e[:-1]):
            word_info = {}
            word_info['text'] = word.text
            word_info['start_time'] = float(word.get("data-stime"))
            word_info['end_time'] = float(e[i + 1].get("data-stime"))
            node['text'].append(word_info)

        word_info = {'text': e[-1].text,
                     'start_time': float(e[-1].get("data-stime")),
                     'end_time': float(next_word)}
        node['text'].append(word_info)
        interventions.append(node)

    element = html_element[0][-1]
    e = element.getchildren()[2].getchildren()
    node = {'voice': element.getchildren()[0].text,
            'start': float(e[0].get("data-stime")),
            'end': float(e[-1].get("data-stime")),
            'text': []}

    for i, word in enumerate(e[:-1]):
        word_info = {'text': word.text,
                     'start_time': float(word.get("data-stime")),
                     'end_time': float(e[i + 1].get("data-stime"))}
        node['text'].append(word_info)

    interventions.append(node)

    return interventions


def get_audio_file(audio_url, path):
    """
    TODO DOCUMENTATION
    :param audio_url:
    :param path:
    :return:
    """
    extension = audio_url.split('.')[-1]
    r = requests.get(audio_url, timeout=30)
    filename = os.path.join(path, 'audio.' + extension)
    open(filename, 'wb').write(r.content)
    return filename


def save_trans(trans, path):
    """
    TODO DOCUMENTATION
    :param trans:
    :param path:
    :return:
    """
    filename = os.path.join(path, 'trans.json')
    open(filename, 'wb').write(
        simplejson.dumps(trans, indent=4, ensure_ascii=False).replace("'", '"').encode('utf8'))
    return filename


def get_ip():
    """
    TODO DOCUMENTATION
    :return:
    """
    return socket.gethostbyname(socket.gethostname())