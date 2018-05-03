# import time
import json
import os

from models.business.WebScrapping import WebScrapping


class ScrapeController:

    def __init__(self):
        self.__all_urls = None

    def __get_all_urls(self):
        file_directory = "./"
        for file in os.listdir(file_directory):
            if file.endswith(".json"):
                with open(os.path.join(file_directory, file), 'r') as content_file:
                    self.__all_urls = json.loads(content_file.read())

    def scrape_now(self):
        self.__get_all_urls()
        web_scrapping = WebScrapping()
        for url in self.__all_urls['pages']:
            print(url)
            web_scrapping.automatic_scrape(False, "../scrape_pages/Amazon/", url)
            # time.sleep(20)
