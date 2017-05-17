import nltk

def unigram(title, vector):
    """ Unigram features. """

    word_list = nltk.word_tokenize(title)
    for word in word_list:
        vector["has({})".format(word)] = True

def bigram(title, vector):
    word_list = nltk.word_tokenize(title)
    bigrams = nltk.bigrams(word_list)
    for bigram in bigrams:
        vector["has({})".format(bigram)] = True

def taggedWords(title, vector):
    word_list = nltk.word_tokenize(title)
    taggedwords = nltk.pos_tag(word_list)
    for taggedword in taggedwords:
        vector["has({})".format(taggedword)] = True

def posTags(title, vector):
    word_list = nltk.word_tokenize(title)
    taggedwords = nltk.pos_tag(word_list)
    for taggedword in taggedwords:
        vector["has POS ({})".format(taggedword[1])] = True

def firstFive(title, vector):
    word_list = nltk.word_tokenize(title)
    for i in range(0, min(len(word_list), 5)):
        vector["has ({}) in first-five".format(word_list[i])] = True

def colocWords(title, vector):
    word_list = nltk.word_tokenize(title)
    for i in range(0, len(wordlist)):
        vector["has ({}) at ({})".format(wordlist[i], i)] = True


def colocPos(title, vector):
    word_list = nltk.word_tokenize(title)
    taggedwords = nltk.pos_tag(word_list)
    for i in range(0, len(taggedwords)):
        vector["has ({}) at ({})".format(taggedwords[i][1], i)] = True

def colocWordsPos(title, vector):
    word_list = nltk.word_tokenize(title)
    taggedwords = nltk.pos_tag(word_list)
    for i in range(0, len(taggedwords)):
        vector["has ({}) at ({})".format(taggedwords[i][1], i)] = True

def caps(title, vector):
    word_list = nltk.word_tokenize(title)
    num_caps = 0
    for word in word_list:
        if word.isupper():
            num_caps += 1
    vector["has ({}) capitalized words".format(num_caps)] = True


feature_map = {
    'unigram': unigram,
    'bigram': bigram,
    'taggedWords': taggedWords,
    'posTags': posTags,
    'firstFive': firstFive,
    'colocWords': colocWords,
    'colocPos': colocPos,
    'colocWordsPos':colocWordsPos,
    'caps':caps


}
