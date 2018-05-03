from models.business.BagOfWords import BagOfWords
from controllers.ScrapeController import ScrapeController

bg = BagOfWords()
bg.main_execution()

scrp = ScrapeController()
# scrp.scrape_now()
