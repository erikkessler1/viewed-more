import argparse
import nltk
import pickle
from features import feature_map
from csv import DictReader

""" Tool for training a classifier.

Allows user to specify the classifier type, feature set, and optionally a save location.
Either use the command line tool or call the train method directly.

"""

def read_labled_titles(filename):
    """ Reads a CSV file and returns list of labled titles.

    Args:
      filename (string): path to the file
    Returns:
      [(string, string)]: list of tuples with title and label
    """
    with open(filename) as file:
        reader = DictReader(file)
        return [(row["title"], row["label"]) for row in reader]

def generate_feature_vector(title, features):
    """ Creates feature vector from list of features.

    Args:
      title (string): the title to generate features for 
      features: list of method names that add features to existing feature vector
    Returns:
      {string : value}: feature vector for the title
    """
    feature_vector = {}
    for feature_name in features:
        if feature_name in feature_map:
            feature_map[feature_name](title, feature_vector)
    return feature_vector

def save_classifier(classifier, location):
    """ Saves a classifier to the location specified.

    Args:
      classifier: the classifier to save
      location: path to file where wish to save the classifier
    """
    with open(location, 'wb') as save_file:
        pickle.dump(classifier, save_file)
    
def train(training_filename, classifier_type, features, save_location=None):
    """ Train a classifier with a set of features. 

    Args:
      training_filename (string): location of the training CSV file
      classifer_type: NTLK classifier type (ex. Naive Bayes)
      features (list(string)): list of features to use
      save_location (string): optional location to save the classifier
    Returns:
      the trained classifier
    """
    labeled_titles = read_labled_titles(training_filename)
    labeled_vectors = [(generate_feature_vector(title, features), label) for (title, label) in labeled_titles]
    classifier = classifier_type.train(labeled_vectors)

    if save_location:
        save_classifier(classifier, save_location)
        
    return classifier

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a classifier.')
    parser.add_argument('training_file', help='CSV file with labeled titles')
    parser.add_argument('-b', dest='classifier_type', action='store_const', const=nltk.NaiveBayesClassifier, default=nltk.NaiveBayesClassifier, help='use a Naive Bayes classifier')
    parser.add_argument('-f', dest='features', help='comma separated list of features to use', required=True)
    parser.add_argument('-s', dest='save_location', help='location to save the classifier')

    args = parser.parse_args()

    train(args.training_file, args.classifier_type, args.features.split(','), args.save_location)

