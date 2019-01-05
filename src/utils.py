import requests
from os import path


def get_file(url):
    """
    TODO DOCUMENTATION
    :param url:
    :type url: str
    :return:
    """
    response = requests.get(url, allow_redirects=True)
    filename = url.split('/')[-1]
    print(filename)
    open(path.join('downloads', filename), 'wb').write(response.content)
