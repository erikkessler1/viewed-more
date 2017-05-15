import csv
import nltk
import html
from collections import defaultdict


def unigramVector(title):
    """Starts with a list of good titles, (uploader, id, title, views, age, upmean, upsd, devs)
    creates a starting dictionary for the bag of words approach"""

    dictionary = {}
    processed_title = html.unescape(title[2])
    tw_list = nltk.word_tokenize(processed_title)
    for word in tw_list:
        dictionary[word] = True



    return dictionary

def createVector(title, alltitles):
    """Creates a vector"""
    for word in title:
        alltitles[word] = True

    return alltitles

def allTitles(path):
    """splits the dictionary and returns both a list of good titles and a list of bad ones."""
    with open(path, 'r') as f:

        reader = csv.reader(f)
        uploader_list = list(reader)
        del uploader_list[0]

    return uploader_list
    #uploader_dict = create_uploader_dict(reader)
    # good_titles = []
    # bad_titles = []
    #
    #
    #
    # for i in range(1, len(uploader_list)): #uploader_dict:
    #     video = uploader_list[i]
    #
    #     if float(video[7]) > 0:
    #         good_titles.append([video])
    #
    #     elif float(video[7]) < 0:
    #         bad_titles.append([video])
    #
    #
    # return good_titles, bad_titles


def create_list(reader):
    """ Create map from uploader to videos from the CSV reader.

    Args:
      reader (DictReader): CSV reader with headser for uploader, title, and views
    Returns:
      {string: [(string, string, int, string, int, int,int)]}: Dict from uploader to list of video id, title, views, age tuples.
    """
    uploader_dict = defaultdict(list)
    for row in reader:
        uploader_dict[row["uploader"]].append((row["id"], row["title"], int(row["views"]), row["age"], row["uploader_mean"], row ["uploader_sd"], row["devs"]))
    return uploader_dict


def createFeatures(all_titles):
    features = [] #[Dictionary of features, Label]
    for line in all_titles:
        unigram_feature = unigramVector(line)

        #other features to add in

        feature = unigram_feature # + ...

        #label
        label = "Bad"
        if float(line[7]) >= 0:
            label = "Good"

        features.append(tuple([feature, label]))

    print(features)
    return features


def trainBayes(train):
    features = createFeatures(train)

    classifier = nltk.NaiveBayesClassifier.train(features)
    return classifier

def getTrainTest(alltitles):
    import random
    random.shuffle(alltitles)
    train = alltitles[:int(len(alltitles) * 0.7)]
    test = alltitles[int(len(alltitles) * 0.7):]
    return train, test


##main
if __name__ == "__main__":
    startingdict = "stats.csv"
    all_titles = allTitles(startingdict)
    random_train, random_test = getTrainTest(all_titles)
    test_features = createFeatures(random_test)

    title_classifier = trainBayes(random_train)
    print(nltk.classify.accuracy(title_classifier, test_features))










# def containsQorEx(title, alltitles):
#     """if the title contains a question or an exclamation, add it in"""
#     if title.contains("?"):
#         alltitles["ends_q"] = True
#     else:
#         alltitles["ends_q"] = False
#
#     if title.contains("!"):
#         alltitles["ends_ex"] = True
#     else:
#         alltitles["ends_ex"] = False
