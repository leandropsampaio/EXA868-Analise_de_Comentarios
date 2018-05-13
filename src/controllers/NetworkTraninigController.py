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

    def __execute_bag_of_words(self, data_set):
        self.__bag_of_words = BagOfWords(data_set)
        return self.__bag_of_words.main_execution()

    def __split_base(self):
        complete_base = self.__database_controller.get_reviews()
        complete_bag_of_words = self.__execute_bag_of_words(complete_base)
        complete_base_length = len(complete_bag_of_words)
        training_set_length = int(complete_base_length * 0.8)
        # test_set_length = complete_base_length - training_set_length
        self.__training_set = complete_bag_of_words[:training_set_length]
        self.__test_set = complete_bag_of_words[training_set_length:]

    def create_neural_network(self):
        self.__split_base()
        self.__nn = NeuralNetwork(self.__bag_of_words.get_unique_words(), len(self.__training_set))

    def start_training(self):
        self.__nn.training_network(self.__training_set, 25)

    def test_neural_network(self):
        self.__nn.test_network(self.__test_set)

    def save_nn(self):
        self.__nn.save_network('emotions_nn.xml')

    def load_nn(self):
        self.__nn.load_network('emotions_nn.xml')
