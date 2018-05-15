from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised import BackpropTrainer
from pybrain3.tools.shortcuts import buildNetwork
from pybrain3.tools.xml.networkreader import NetworkReader
from pybrain3.tools.xml.networkwriter import NetworkWriter


# from pybrain.tools.customxml.networkwriter import NetworkWriter
# from pybrain.tools.customxml.networkreader import NetworkReader


class NeuralNetwork:
    def __init__(self, unique_words, total_comments, hidden=400):
        self._max_value = 0.9
        self._min_value = 0.1
        self.__unique_words = unique_words
        self.__total_comments = total_comments
        self.__conversion_rate = 0.5
        print("Total de Comentários: ", self.__total_comments)
        print("Total de Palavras Únicas: ", len(self.__unique_words))

        unique_words_length = len(self.__unique_words)
        # Construcao da rede com quantPalavrasUnicas na entradas, 1000 camadas ocultas e 1 sai­da
        self.__network = buildNetwork(unique_words_length, hidden, 1)
        # Base de dados com quantPalavrasUnicas atributos prevzisores e uma clase
        self.__base = SupervisedDataSet(unique_words_length, 1)
        '''
        self.__network = buildNetwork(2, 3, 1, outclass = SoftmaxLayer,
                            hiddenclass = SigmoidLayer, bias = False)
        print(self.__network['in'])
        print(self.__network['hidden0'])
        print(self.__network['out'])
        print(self.__network['bias'])
        '''

    def float_round(self, number, close_to):
        """import math
        return math.isclose(float(number), close_to, abs_tol=0.45)"""
        if float(number) >= 0.5:
            return self._max_value == close_to
        else:
            return self._min_value == close_to

    def __add_training_set(self, training_base):

        # Adicionando os dados (Entrada), (Classe) para o treinamento
        for index in range(0, self.__total_comments):
            training_set_length = 2500  # int(self.__total_comments * 0.8)
            if index < training_set_length:
                array = []
                # ********************** TROCAR PELO ARRAY DE ENTRADAS *******************
                entry_array = training_base[index][0]

                if training_base[index][1] >= 3.5:
                    comment_class = self._max_value
                else:
                    comment_class = self._min_value

                    # print(entry_array, comment_class)
                for key in entry_array:
                    # print (entry_array[key])
                    array.append(entry_array[key])

                self.__base.addSample(array, comment_class)

        # Imprimir a entrada e a classe supervisionada
        # print(base['input'])
        # print(base['target'])

    def training_network(self, training_base, number_of_trainings=20):

        print("Start Training")
        self.__add_training_set(training_base)
        training = BackpropTrainer(self.__network, dataset=self.__base, learningrate=0.01, momentum=0.06)

        # Fazer o treinamento number_of_trainings vezes e mostrar o erro
        '''for count in range(0, number_of_trainings):
                print("Training Number %d" % count + 1)
                print("Error %s" % training.train())'''
        # above, use training with validation
        training.trainUntilConvergence(maxEpochs=number_of_trainings, verbose=True, validationProportion=0.25)

    def test_network(self, test_base):
        # self.__network = NetworkReader.readFrom('filename.xml')
        test_base_length = len(test_base)
        corrects = 0
        errors = 0
        # ******************* PASSAR OS COMENTÁRIOS PARA O TESTE *********************
        for index in range(0, test_base_length):
            array = []
            # ********************** TROCAR PELO ARRAY DE ENTRADAS *******************
            entry_array = test_base[index][0]

            if test_base[index][1] >= 3.5:
                comment_class = self._max_value
            else:
                comment_class = self._min_value

                # print(entry_array, comment_class)
            for key in entry_array:
                array.append(entry_array[key])
            try:
                found = self.__network.activate(array)
                if self.float_round(found, comment_class):
                    corrects += 1
                else:
                    errors += 1
                print(found, comment_class, self.float_round(found, comment_class))
            except (AssertionError, IndexError) as error:
                print("Have an error message: %s" % error)
        print("%f%%" % ((corrects * 100) / (errors + corrects)))

    def save_network(self, location):
        NetworkWriter.writeToFile(self.__network, location)

    def load_network(self, location):
        self.__network = NetworkReader.readFrom(location)
