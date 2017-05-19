import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

""" Colloection of different features. """

def unigram(title, vector):
    word_list = nltk.word_tokenize(title)
    for word in word_list:
        vector["has({})".format(word)] = True

def unigramNoStop(title, vector):
    word_list = nltk.word_tokenize(title)
    stop = set(stopwords.words('english'))
    for word in word_list:
        if word not in stop:
             vector["has({})".format(word)] = True

def bigram(title, vector):
    word_list = nltk.word_tokenize(title)
    bigrams = nltk.bigrams(word_list)
    for bigram in bigrams:
        vector["has({})".format(bigram)] = True

def taggedWords(title, vector):
    word_list = nltk.word_tokenize(title)
    taggedwords = nltk.pos_tag(word_list)
    stop = set(stopwords.words('english'))

    for taggedword in taggedwords:
        if taggedword[0] not in stop:
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
    for i in range(0, len(word_list)):
        vector["has ({}) at ({})".format(word_list[i], i)] = True

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

def lengthOfTitle(title, vector):
    word_list = nltk.word_tokenize(title)
    num_words = len(word_list)
    vector["has ({}) number of words".format(num_words)] = True


# Experimental and incomplete feaure that looks at Google Trend data
# see future work section of report for more.
pytrends = None
def mostPopularKeywords(title, vector):
    global pytrends
    if not pytrends:
        from pytrends.request import TrendReq
        from pytrends.request import TrendReq
        google_username = "NLPProject2017"
        google_password = "JonPark2017"
        pytrends = TrendReq(google_username, google_password, hl='en-US', tz=360, custom_useragent=None)

    rel_sum_of_indices = 0
    abs_sum_of_indices = 0

    stop = set(stopwords.words('english'))
    word_list = nltk.word_tokenize(title)
    for word in word_list:
        if word not in stop:
            word = word.lower()
            syns = list(set([word] + [y.lemma_names()[0] for y in wn.synsets(word)] ))
            kw_list = syns[0:min(5, len(syns))]
            if len(kw_list) > 1:
                pytrendsbuild = pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
                results = [(keyword, pytrends.interest_over_time().iloc[-1][keyword]) for keyword in kw_list]

                results.sort(key=lambda x: (-x[1]))
                try:
                    index = [x for x, y in enumerate(results) if y[0].lower() == word.lower()][0]
                except:
                    index = 4

                rel_sum_of_indices += 1/(int(index) + 1)
                abs_sum_of_indices += pytrends.interest_over_time().iloc[-1][word]



    vector["Sum of relative indexed popularity: {}".format(rel_sum_of_indices)] = True
    print(rel_sum_of_indices, abs_sum_of_indices)
    vector["Sum of absolute indexed popularity: {}".format(abs_sum_of_indices)] = True





feature_map = {
    'unigram': unigram,
    'bigram': bigram,
    'taggedWords': taggedWords,
    'posTags': posTags,
    'firstFive': firstFive,
    'colocWords': colocWords,
    'colocPos': colocPos,
    'colocWordsPos':colocWordsPos,
    'caps':caps,
    'mostPopular': mostPopularKeywords,
    'unigramNoStop':unigramNoStop
}
