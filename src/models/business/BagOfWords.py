import re
from unicodedata import normalize

import nltk


# nltk.download("stopwords")
# nltk.download("rslp")


class BagOfWords:

    def __init__(self, base):
        # Base de dados com as frases
        self.__base = base
        self.__unique_words = None
        self.__frequency = None
        # --------------------------------------- Remoção de stop words ------------------------------------------------
        # Pegando as palavras (stopwords) da biblioteca
        self.stopwordsnltk = nltk.corpus.stopwords.words('portuguese')
        self.stopwordsnltk.append("é")
        self.__one_time = None

    def __remove_accentuation(self, txt):
        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

    def __remove_special_characters(self, frase):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', frase)

        removal_list = ["\?+", "!+", "\.+", ",+", "\(+", "\)+"]

        for pattern in removal_list:
            cleaner = re.compile(pattern)
            clean_text = re.sub(cleaner, "", clean_text)
        return clean_text

    # Método para pecorrer todas as palavras da base de dados e remover as stopwords
    def __remove_stop_word(self, text):
        phrases = []

        for words, emotion in text:
            without_stop = [p for p in
                            self.__remove_special_characters(self.__remove_accentuation(words.lower())).split() if
                            p not in self.stopwordsnltk]
            phrases.append((" ".join(str(x) for x in without_stop), emotion))
        return phrases

    # ------------------------------- Extração do radical das palavras (stemming) --------------------------------------

    # Remover a raiz das palavras, ficando apenas com o radical
    def __apply_stemmer(self, texto):
        stemmer = nltk.stem.RSLPStemmer()
        stemming_phrases = []

        for words, emotion in texto:
            com_stemming = [str(stemmer.stem(p)) for p in words.split() if p not in self.stopwordsnltk]
            stemming_phrases.append((com_stemming, emotion))
        return stemming_phrases

    # ----------------------------------- Listagem de todas as palavras da base ----------------------------------------

    # Buscando todas as palavras, sem a emoção
    def __search_words(self, phrase):
        all_words = []

        for (words, emocao) in phrase:
            all_words.extend(words)
        return all_words

    # ------------------------------------------ Extração de palavras únicas -------------------------------------------

    # Buscando a frequência das palavras
    def __search_frequency(self, words):
        # nltk.FreqDist(palavras) - Retorna a quantidade de vezes que a palavra apareceu
        words = nltk.FreqDist(words)
        return words

    def _words_that_appear_just_few_times(self, words):
        one_time = []
        for word in words.keys():
            if words[word] < 4:
                one_time.append(word)
        self.__one_time = tuple(one_time)

    # Através da quantidade de vezes e da palavra, esse método pega apenas as palavras ou seja as chaves da lista (Keys)
    def __search_unique_words(self, frequency):
        returned_frequency = []
        frequency_keys = frequency.keys()
        for word in frequency_keys:
            if word not in self.__one_time:
                returned_frequency.append(word)
        return tuple(returned_frequency)

    # -------------------------------------- Extração das palavras de cada frase ---------------------------------------

    def __words_extractor(self, document):
        characteristics = {}
        frequency = self.__search_frequency(document)
        for words in self.__unique_words:
            if words in document:
                characteristics[words] = frequency[words]
            else:
                characteristics[words] = 0
        return characteristics

    def main_execution(self):
        # Imprimindo as palavras sem a raiz e sem as stopwords
        stemming_words = self.__apply_stemmer(self.__remove_stop_word(self.__base))

        words = self.__search_words(stemming_words)
        # print(palavras)

        self.__frequency = self.__search_frequency(words)
        # Mostra a quantidade de vezes que a palavra apareceu, junto com a palavra
        # method to determines words to delete from unique words list
        self._words_that_appear_just_few_times(self.__frequency)

        self.__unique_words = self.__search_unique_words(self.__frequency)
        # Imprime na tela as palavras sem repetição ou seja apenas uma vez cada palavra

        complete_base = nltk.classify.apply_features(self.__words_extractor, stemming_words)

        return complete_base

    def get_unique_words(self):
        return self.__unique_words
