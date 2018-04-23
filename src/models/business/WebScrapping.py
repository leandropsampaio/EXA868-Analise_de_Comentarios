import requests
from bs4 import BeautifulSoup


class WebScrapping:

    def __init__(self):
        self.__itemPage = []
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        self.__url = "http://amazon.com.br/"
        self.__currentCommentPage = 1
        self.__soup = None

    def seturl(self, url):
        self.__url = url

    def __getpage(self):
        response = requests.get(("%s&pageNumber=2%d" % (self.__url, self.__currentCommentPage)), headers=self.__headers)
        self.__soup = BeautifulSoup(response.text)

    def scrapdiv(self):
        self.__getpage()
        #print(self.__soup)
        for value in self.__soup.find('div', class_='a-section a-spacing-none review-views celwidget'):
            print(value)
