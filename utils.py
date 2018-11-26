import requests
from os import path


def get_file(url):
    """

    :param url:
    :type url: str
    :return:
    """
    response = requests.get(url, allow_redirects=True)
    filename = url.split('/')[-1]
    print(filename)
    open(path.join('downloads', filename), 'wb').write(response.content)


if __name__ == '__main__':
    get_file(
        'https://prisa-es.mc.tritondigital.com/HOY_POR_HOY_CADENASER_222_P/media/2018/11/23/cadenaser_hoyporhoy_20181123_100000_110000.mp3')
