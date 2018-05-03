import requests
from itertools import cycle
from lxml.html import fromstring


class ProxyScrapper:

    def __init__(self):
        self.__proxies = None
        self.__proxy_pool = None

    def __get_proxies(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:80]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies

    def run(self):
        self.__proxies = self.__get_proxies()
        self.__proxy_pool = cycle(self.__proxies)

    def get_proxy_pool(self):
        return self.__proxy_pool
