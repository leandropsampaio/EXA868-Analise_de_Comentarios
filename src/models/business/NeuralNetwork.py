from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised import BackpropTrainer
from pybrain3.tools.shortcuts import buildNetwork

from pybrain3.tools.xml.networkwriter import NetworkWriter
from pybrain3.tools.xml.networkreader import NetworkReader


# from pybrain.tools.customxml.networkwriter import NetworkWriter
# from pybrain.tools.customxml.networkreader import NetworkReader


class NeuralNetwork:
    def __init__(self, unique_words, total_comments):
        self.__unique_words = unique_words
        self.__total_comments = total_comments
        self.__conversion_rate = 0.5
        print("Total de Comentários: ", self.__total_comments)
        print("Total de Palavras Únicas: ", len(self.__unique_words))

        unique_words_length = len(self.__unique_words)
        # Construcao da rede com quantPalavrasUnicas na entradas, 1000 camadas ocultas e 1 sai­da
        self.__network = buildNetwork(unique_words_length, 200, 1)
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

    def __convert_string_to_number(self, received_string):
        converted_string = 1
        count = 1
        for character in received_string:
            count += self.__conversion_rate
            converted_string += (ord(character) * count)
        return converted_string

    def __add_training_set(self, training_base):

        # Adicionando os dados (Entrada), (Classe) para o treinamento
        for index in range(0, self.__total_comments):
            training_set_length = 2500  # int(self.__total_comments * 0.8)
            if index < training_set_length:
                array = []
                # ********************** TROCAR PELO ARRAY DE ENTRADAS *******************
                entry_array = training_base[index][0]
                # ********************** TROCAR PELO CLASSE ******************************
                comment_class = training_base[index][1]

                # print(entry_array, comment_class)
                for key in entry_array:
                    # print (entry_array[key])
                    array.append(entry_array[key])

                self.__base.addSample(array, comment_class)

                # for key in entry_array.keys():
                #    print("ENTRADA: " + str(entry_array[key]))
                #    print("SAIDA: " + str(comment_class))
                # Adicionando o comentário na base
                # print((self.__convert_string_to_number(key), entry_array[key]))
                #   self.__base.addSample((self.__convert_string_to_number(key), entry_array[key]), comment_class)

        # Imprimir a entrada e a classe supervisionada
        # print(base['input'])
        # print(base['target'])

    def training_network(self, training_base, number_of_trainings=20):

        self.__add_training_set(training_base)
        training = BackpropTrainer(self.__network, dataset=self.__base, learningrate=0.01, momentum=0.06)

        # Fazer o treinamento number_of_trainings vezes e mostrar o erro
        for i in range(0, number_of_trainings):
            print("TREINO %d" % i)
            error = training.train()
            print("Erro: %s" % error)

    def test_network(self, test_base):
        # self.__network = NetworkReader.readFrom('filename.xml')
        test_base_length = len(test_base)
        # ******************* PASSAR OS COMENTÁRIOS PARA O TESTE *********************
        for index in range(0, test_base_length):
            array = []
            # ********************** TROCAR PELO ARRAY DE ENTRADAS *******************
            entry_array = test_base[index][0]
            # ********************** TROCAR PELO CLASSE ******************************
            comment_class = test_base[index][1]

            # print(entry_array, comment_class)
            for key in entry_array:
                array.append(entry_array[key])
            try:
                print(self.__network.activate(array), comment_class)
            except (AssertionError, IndexError) as error:
                print("Have an error message: %s" % error)

    def save_network(self, location):
        NetworkWriter.writeToFile(self.__network, location)

    def load_network(self, location):
        self.__network = NetworkReader.readFrom(location)
