import re

import nltk

from unicodedata import normalize
from models.business.DatabaseController import DatabaseController


# nltk.download("stopwords")
# nltk.download("rslp")


class BagOfWords:

    def __init__(self):
        # Base de dados com as frases
        self.base = DatabaseController().get_reviews()
        self.palavrasUnicas = None
        self.__frequencia = None
        # --------------------------------------- Remoção de stop words ------------------------------------------------
        # Pegando as palavras (stopwords) da biblioteca
        self.stopwordsnltk = nltk.corpus.stopwords.words('portuguese')
        self.stopwordsnltk.append("é")

    def __remover_acentos(self, txt):
        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

    def __removerCaracteresEspeciais(self, frase):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', frase)

        lista_remocao = ["\?+", "!+", "\.+", ",+", "\(+", "\)+"]

        for pattern in lista_remocao:
            cleaner = re.compile(pattern)
            clean_text = re.sub(cleaner, "", clean_text)
        return clean_text

    # Método para pecorrer todas as palavras da base de dados e remover as stopwords
    def removeStopWord(self, texto):
        frases = []

        for palavras, emocao in texto:
            semStop = [p for p in self.__removerCaracteresEspeciais(self.__remover_acentos(palavras.lower())).split() if
                       p not in self.stopwordsnltk]
            frases.append((" ".join(str(x) for x in semStop), emocao))
        return frases

    # ------------------------------- Extração do radical das palavras (stemming) --------------------------------------

    # Remover a raiz das palavras, ficando apenas com o radical
    def aplicaStemmer(self, texto):
        stemmer = nltk.stem.RSLPStemmer()
        frasesStemming = []

        for palavras, emocao in texto:
            comStemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in self.stopwordsnltk]
            frasesStemming.append((comStemming, emocao))
        return frasesStemming

    # ----------------------------------- Listagem de todas as palavras da base ----------------------------------------

    # Buscando todas as palavras, sem a emoção
    def buscaPalavras(self, frase):
        todasPalavras = []

        for (palavras, emocao) in frase:
            todasPalavras.extend(palavras)
        return todasPalavras

    # ------------------------------------------ Extração de palavras únicas -------------------------------------------

    # Buscando a frequência das palavras
    def buscaFrequencia(self, palavras):
        # nltk.FreqDist(palavras) - Retorna a quantidade de vezes que a palavra apareceu
        palavras = nltk.FreqDist(palavras)
        return palavras

    # Através da quantidade de vezes e da palavra, esse método pega apenas as palavras ou seja as chaves da lista (Keys)
    def buscaPalavrasUnicas(self, frequencia):
        frequencia = frequencia.keys()
        return frequencia

    # -------------------------------------- Extração das palavras de cada frase ---------------------------------------

    def extratorPalavras(self, documento):
        caracteristicas = {}
        frequencia = self.buscaFrequencia(documento)
        for palavras in self.palavrasUnicas:
            if palavras in documento:
                caracteristicas[palavras] = frequencia[palavras]
            else:
                caracteristicas[palavras] = 0
        return caracteristicas

    def main_execution(self):
        # Imprimindo as palavras sem a raiz e sem as stopwords
        frasesComStemming = self.aplicaStemmer(self.removeStopWord(self.base))
        # print(frasesComStemming)

        # Imprimindo todas as palavras das frases, sem a emoção
        palavras = self.buscaPalavras(frasesComStemming)
        # print(palavras)

        self.__frequencia = self.buscaFrequencia(palavras)
        # Mostra a quantidade de vezes que a palavra apareceu, junto com a palavra
        # print(self.__frequencia.most_common(50))

        self.palavrasUnicas = self.buscaPalavrasUnicas(self.__frequencia)
        # Imprime na tela as palavras sem repetição ou seja apenas uma vez cada palavra
        # print(self.palavrasUnicas)

        baseCompleta = nltk.classify.apply_features(self.extratorPalavras, frasesComStemming)
        print(baseCompleta)
