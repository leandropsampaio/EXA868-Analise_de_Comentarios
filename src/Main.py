"""
from controllers.ScrapeController import ScrapeController
scrap = ScrapeController()
scrap.scrape_now()
"""
import time

from controllers.NetworkTraninigController import NetworkTrainingController

nnc = NetworkTrainingController()
nnc.create_neural_network()
# nnc.load_nn()

start_time = time.time()
nnc.start_training()
print("--- %s seconds ---" % (time.time() - start_time))

nnc.test_neural_network()
nnc.save_nn()
