import os
import re
import requests
from bs4 import BeautifulSoup

from models.business.ProxyScrapper import ProxyScrapper
from controllers.DatabaseController import DatabaseController


class WebScrapping:

    def __init__(self):
        self.__itemPage = []
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.71 Safari/537.36 '
        }
        self.__url = "http://amazon.com.br/"
        self.__currentCommentPage = 1
        self.__soup = None
        self.__scrapeResults = []
        self.__database = DatabaseController()
        self.__proxy_scrapper = ProxyScrapper()
        self.__proxy_scrapper.run()
        self.__proxy_pool = self.__proxy_scrapper.get_proxy_pool()

    def set_url(self, url):
        self.__url = url

    def __get_page(self):
        proxy = next(self.__proxy_pool)
        response = requests.get(("%s&pageNumber=%d" % (self.__url, self.__currentCommentPage)), headers=self.__headers,
                                proxies={"http": proxy, "https": proxy})
        self.__soup = BeautifulSoup(response.text, "html.parser")

    def __remove_tags(self, string_with_tag):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', string_with_tag)
        return clean_text

    def __more_deep_scrape(self):
        temporary_result_list = []
        for value in self.__scrapeResults:
            temporary_soup = BeautifulSoup(str(value), "html.parser")
            temporary_string = ""
            try:
                temporary_rating = None
                for rating in temporary_soup.find('span', class_='a-icon-alt'):
                    temporary_rating = rating
                for onlyComment in temporary_soup.find('span', class_='a-size-base review-text'):
                    temporary_string += str(onlyComment)
                temporary_result_list.append((str(temporary_rating), self.__remove_tags(temporary_string)))
            except TypeError as error:
                print("Type error({0})".format(error))
        self.__scrapeResults = temporary_result_list

    def __scrap_div(self):

        for value in self.__soup.find('div', class_='a-section a-spacing-none review-views celwidget'):
            self.__scrapeResults.append(value)

        self.__more_deep_scrape()
        self.__database.insert_reviews(self.__scrapeResults)

    def have_next_page(self):
        print("Entering have next")
        try:
            for value in self.__soup.find('ul', class_='a-pagination'):
                try:
                    verify = int(value.text)
                    if self.__currentCommentPage < verify:
                        return True
                except ValueError as error:
                    print(error)
        except TypeError as error:
            print(error)
            print(self.__soup)
        return False

    def automatic_scrape(self, from_file=False, file_directory=None, first_url=""):
        if from_file:
            for file in os.listdir(file_directory):
                if file.endswith(".html"):
                    with open(os.path.join(file_directory, file), 'r') as content_file:
                        self.__soup = BeautifulSoup(content_file.read(), "html.parser")
                    self.__scrap_div()

        elif not from_file:
            self.set_url(first_url)
            self.__get_page()

            while self.have_next_page():
                self.__currentCommentPage += 1
                self.__scrap_div()
                try:
                    self.__get_page()
                except:
                    '''
                    Most free proxies will often get connection errors. You will have retry the entire request using
                    another proxy to work. We will just skip retries as its beyond the scope of this tutorial and
                    we are only downloading a single url
                    '''
                    print("Skipping. Connection error")
