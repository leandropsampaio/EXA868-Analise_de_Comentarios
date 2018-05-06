'''Ubuntu Imports'''
from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised import BackpropTrainer
from pybrain3.tools.shortcuts import buildNetwork

'''Windows Imports'''


# from pybrain.datasets import SupervisedDataSet
# from pybrain.supervised.trainers import BackpropTrainer
# from pybrain.structure.modules import SoftmaxLayer
# from pybrain.structure.modules import SigmoidLayer

class NeuralNetwork:
    def __init__(self, unique_words, total_comments):
        self.__unique_words = unique_words
        self.__total_comments = total_comments

        unique_words_length = 2  # len(self.__unique_words)
        # Construcao da rede com quantPalavrasUnicas na entradas, 1400 camadas ocultas e 1 sai­da
        self.__network = buildNetwork(unique_words_length, 2, 1)
        # Base de dados com quantPalavrasUnicas atributos previsores e uma clase
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
        converted_string = 0.1
        count = 1
        for character in received_string:
            count += 0.1
            converted_string += (ord(character) * count)
        return converted_string

    def __add_training_set(self, training_base):
        # Adicionando os dados (Entrada), (Classe) para o treinamento
        for index in range(0, self.__total_comments):
            # ********************** TROCAR PELO ARRAY DE ENTRADAS *******************
            entry_array = training_base[index][0]
            # ********************** TROCAR PELO CLASSE ******************************
            comment_class = training_base[index][1]

            for key in entry_array.keys():
                # Adicionando o comentário na base
                if entry_array[key] > 3:
                    print((self.__convert_string_to_number(key), entry_array[key]))
                    self.__base.addSample((self.__convert_string_to_number(key), entry_array[key]), comment_class)

        # Imprimir a entrada e a classe supervisionada
        # print(base['input'])
        # print(base['target'])

    def training_network(self, training_base):
        self.__add_training_set(training_base)
        training = BackpropTrainer(self.__network, dataset=self.__base, learningrate=0.01, momentum=0.06)

        # Fazer o treinamento 30000 vezes e mostrar o erro
        for i in range(1, 30000):
            print(i)
            error = training.train()
            if i % 1000 == 0:
                print("Erro: %s" % error)

    def test_network(self, test_base):
        # ************************** PARTE DOS TESTES ********************************
        # Testar as entradas e ver a saí­da da rede neural

        # ******************* PASSAR OS COMENTÁRIOS PARA O TESTE *********************
        for index in range(0, len(test_base)):
            entry_array = test_base[index][0]

            for key in entry_array.keys():
                print(key, self.__network.activate([self.__convert_string_to_number(key), entry_array[key]]))
