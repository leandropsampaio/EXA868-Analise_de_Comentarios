import nltk
#nltk.download("stopwords")
#nltk.download("rslp")

# Base de dados com as frases
base = [('eu sou admirada por muitos','alegria'),
        ('me sinto completamente amado','alegria'),
        ('amar e maravilhoso','alegria'),
        ('estou me sentindo muito animado novamente','alegria'),
        ('eu estou muito bem hoje','alegria'),
        ('que belo dia para dirigir um carro novo','alegria'),
        ('o dia está muito bonito','alegria'),
        ('estou contente com o resultado do teste que fiz no dia de ontem','alegria'),
        ('o amor e lindo','alegria'),
        ('nossa amizade e amor vai durar para sempre', 'alegria'),
        ('estou amedrontado', 'medo'),
        ('ele esta me ameacando a dias', 'medo'),
        ('isso me deixa apavorada', 'medo'),
        ('este lugar e apavorante', 'medo'),
        ('se perdermos outro jogo seremos eliminados e isso me deixa com pavor', 'medo'),
        ('tome cuidado com o lobisomem', 'medo'),
        ('se eles descobrirem estamos encrencados', 'medo'),
        ('estou tremendo de medo', 'medo'),
        ('eu tenho muito medo dele', 'medo'),
        ('estou com medo do resultado dos meus testes', 'medo')]

# Retorna o registro da matriz na posição 0
#print(base[0])

# --------------------------------------- Remoção de stop words -------------------------------------------------------
# Stopwords manual
stopwords = ['a', 'agora', 'algum', 'alguma', 'aquele', 'aqueles', 'de', 'deu', 'do', 'e', 'estou', 'esta', 'esta',
             'ir', 'meu', 'muito', 'mesmo', 'no', 'nossa', 'o', 'outro', 'para', 'que', 'sem', 'talvez', 'tem', 'tendo',
             'tenha', 'teve', 'tive', 'todo', 'um', 'uma', 'umas', 'uns', 'vou']

# Pegando as palavras (stopwords) da biblioteca
stopwordsnltk = nltk.corpus.stopwords.words('portuguese')

# Imprimindo as stopwords da biblioteca nltk
print(stopwordsnltk)

# Método para pecorrer todas as palavras da base de dados e remover as stopwords
def removeStopWord(texto):
    frases = []

    for(palavras, emocao) in texto:
        semStop = [p for p in palavras.split() if p not in stopwordsnltk]
        frases.append((semStop, emocao))
    return frases

# Imprimindo as palavras da frase, removendo as stopwords da biblioteca nltk
#print(removeStopWord(base))

# ------------------------------- Extração do radical das palavras (stemming) -----------------------------------------

# Remover a raiz das palavras, ficando apenas com o radical
def aplicaStemmer(texto):
    stemmer = nltk.stem.RSLPStemmer()
    frasesStemming = []

    for (palavras, emocao) in texto:
        comStemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopwordsnltk]
        frasesStemming.append((comStemming, emocao))
    return frasesStemming

# Imprimindo as palavras sem a raiz e sem as stopwords
frasesComStemming = aplicaStemmer(base)
#print(frasesComStemming)

# ----------------------------------- Listagem de todas as palavras da base -------------------------------------------

# Buscando todas as palavras, sem a emoção
def buscaPalavras(frase):
    todasPalavras = []

    for (palavras, emocao) in frase:
        todasPalavras.extend(palavras)
    return todasPalavras

# Imprimindo todas as palavras das frases, sem a emoção
palavras = buscaPalavras(frasesComStemming)
#print(palavras)

# ------------------------------------------ Extração de palavras únicas ----------------------------------------------

# Buscando a frequência das palavras
def buscaFrequencia(palavras):
    # nltk.FreqDist(palavras) - Retorna a quantidade de vezes que a palavra apareceu
    palavras = nltk.FreqDist(palavras)
    return palavras

frequencia = buscaFrequencia(palavras)
# Mostra a quantidade de vezes que a palavra apareceu, junto com a palavra
print(frequencia.most_common(50))

# Através da quantidade de vezes e da palavra, esse método pega apenas as palavras ou seja as chaves da lista (Keys)
def buscaPalavrasUnicas(frequencia):
    frequencia = frequencia.keys()
    return frequencia

palavrasUnicas = buscaPalavrasUnicas(frequencia)
# Imprime na tela as palavras sem repetição ou seja apenas uma vez cada palavra
print(palavrasUnicas)

# -------------------------------------- Extração das palavras de cada frase -------------------------------------------

def extratorPalavras(documento):
    caracteristicas = {}
    for palavras in palavrasUnicas:
        caracteristicas[palavras] = palavras in documento
    return caracteristicas

caracteristicasFrase = extratorPalavras(['am ', 'nov', 'dia'])
#print(caracteristicasFrase)



baseCompleta = nltk.classify.apply_features(extratorPalavras, frasesComStemming)
print(baseCompleta)









