"""
from controllers.ScrapeController import ScrapeController
scrap = ScrapeController()
scrap.scrape_now()
"""
from controllers.NetworkTraninigController import NetworkTrainingController

nnc = NetworkTrainingController()
nnc.create_neural_network()
# nnc.load_nn()
nnc.start_training()
nnc.test_neural_network()
nnc.save_nn()
