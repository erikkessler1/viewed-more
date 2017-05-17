import nltk

def unigram(title, vector):
    """ Unigram features. """
    
    word_list = nltk.word_tokenize(title)
    for word in word_list:
        vector["has({})".format(word)] = True

feature_map = {
    'unigram': unigram
}
