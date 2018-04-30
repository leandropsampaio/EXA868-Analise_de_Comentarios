import json
import os
import time

from models.business.WebScrapping import WebScrapping
from models.business.BagOfWords import BagOfWords

file_directory = "./"
all_urls = None
for file in os.listdir(file_directory):
    if file.endswith(".json"):
        with open(os.path.join(file_directory, file), 'r') as content_file:
            all_urls = json.loads(content_file.read())

''' count = 0
for url in all_urls['pages']:
    print(url)
    if count <= 7:
        count += 1
        continue
    webscrapping = WebScrapping()
    webscrapping.automatic_scrape(False, "../scrape_pages/Amazon/", url)
    time.sleep(20) '''

bg = BagOfWords()
bg.main_execution()
