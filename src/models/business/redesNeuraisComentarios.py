from pybrain.tools.shortcuts import buildNetwork # Construir rede no automatico
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.structure.modules import SigmoidLayer

'''
rede = buildNetwork(2, 3, 1, outclass = SoftmaxLayer,
                    hiddenclass = SigmoidLayer, bias = False)
print(rede['in'])
print(rede['hidden0'])
print(rede['out'])
print(rede['bias'])
'''

# ************** PASSAR A QUANTIDADE DE PALAVRAS UNICAS ********************** 
quantPalavrasUnicas = 2
# ************** PASSAR A QUANTIDADE DE COMENTARIOS ********************** 
quantComentarios = 2

# Construcao da rede com quantPalavrasUnicas na entradas, 1400 camadas ocultas e 1 sai­da
rede = buildNetwork(quantPalavrasUnicas, 1400, 1)
# Base de dados com quantPalavrasUnicas atributos previsores e uma clase
base = SupervisedDataSet(quantPalavrasUnicas, 1)

# Adicionando os dados (Entrada), (Classe) para o treinamento
for quant in range(0, quantComentarios):
    # ********************** TROCAR PELO ARRAY DE ENTRADAS *******************
    arrayEntradas = (0,1)
    # ********************** TROCAR PELO CLASSE ******************************
    classe = 0
    # Adicionando o comentário na base
    base.addSample(arrayEntradas, classe)
    
# Imprimir a entrada e a classe supervisionada 
#print(base['input'])
#print(base['target'])

# 
treinamento = BackpropTrainer(rede, dataset = base, learningrate = 0.01,
                              momentum = 0.06)

# Fazer o treinamento 30000 vezes e mostrar o erro
for i in range(1, 30000):
    erro = treinamento.train()
    if i % 1000 == 0:
        print("Erro: %s" % erro)


# ************************** PARTE DOS TESTES ********************************
# Testar as entradas e ver a saí­da da rede neural


# ******************* PASSAR OS COMENTÁRIOS PARA O TESTE *********************
print(rede.activate([0, 0]))




