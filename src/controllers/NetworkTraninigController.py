from models.business.BagOfWords import BagOfWords
from models.business.DatabaseController import DatabaseController
from models.business.NeuralNetwork import NeuralNetwork


class NetworkTrainingController:
    def __init__(self):
        self.__nn = None
        self.__database_controller = DatabaseController()
        self.__bag_of_words = None  # BagOfWords()
        self.__training_set = None
        self.__test_set = None

    def __split_base(self):
        complete_base = self.__database_controller.get_reviews()
        complete_base_length = len(complete_base)
        training_set_length = int(complete_base_length * 0.8)
        # test_set_length = complete_base_length - training_set_length
        self.__training_set = complete_base[:training_set_length]
        self.__test_set = complete_base[training_set_length:]

    def __execute_bag_of_words(self):
        self.__bag_of_words = BagOfWords(self.__training_set)
        return self.__bag_of_words.main_execution()

    def create_neural_network(self):
        self.__split_base()
        complete_training_base = self.__execute_bag_of_words()
        self.__nn = NeuralNetwork(self.__bag_of_words.get_unique_words(), len(complete_training_base))
        self.__nn.training_network(complete_training_base)
