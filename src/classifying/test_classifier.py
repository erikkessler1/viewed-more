import argparse
import pickle
from train_classifier import read_labeled_titles, generate_feature_vector
from termcolor import colored

""" Program for testing a classifier against a test file.

Reports metrics and informative features as well.

Useage:
  python test_classifier.py -f FEATURES [-v] [-i INFORMATIVE] <test_file> <classifier>
    -v: Verbose - print all predicts
    -i INFORMATIVE: number of informative features to print
"""

def load_classifier(location):
    """ Loads a classifier from file.

    Args:
      location: path to file
    Returns:
      classifier, features
    """
    with open(location, 'rb') as file:
        return pickle.load(file)

def evaluate(actual_predicts):
    """ Compute accuracy, precision, recall, and f1.

    Args:
      actual_predicts: list of tuples (actual label, predicted label)
    Returns:
      tuple of accuracy, precision, recall, and f1
    """
    tp, tn, fp, fn = 0, 0, 0, 0
    for actual, predict in actual_predicts:
        if actual == 'GOOD':
            if predict == 'GOOD':
                tp += 1
            else:
                fn += 1
        else:
            if predict == 'BAD':
                tn += 1
            else:
                fp += 1

    acc = (tp + tn) / (tp + tn + fp + fn)
    print(tp, fp, tn, fn)
    pre = tp / (tp + fp)
    rec = tp / (tp + fn)
    f1 = (2 * pre * rec) / (pre + rec)

    return (acc, pre, rec, f1)
    
def test(test_file, classifier_location):
    """ Classify titles in test file.

    Args:
      test_file: location of file with labeled titles
      classifier_location: the saved classifier to use
    Returns:
      tuple with predictsion, metrics, and most informative features
    """

    classifier, features = load_classifier(classifier_location)
    labeled_titles = read_labeled_titles(test_file)
    labeled_vectors = [(title, generate_feature_vector(title, features), label) for (title, label) in labeled_titles]

    predictions = [(t, v, l, classifier.classify(v)) for (t, v, l) in labeled_vectors]
    evaluation = evaluate([(t_label, p_label) for _, _, t_label, p_label in predictions])
    most_informative = classifier.most_informative_features(100)

    return (predictions, evaluation, most_informative)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test a classifier.')
    parser.add_argument('test_file', help='CSV file with labeled titles')
    parser.add_argument('classifier', help='file of the classifier')
    parser.add_argument('-v', dest='verbose', action='store_true', help='print full information')
    parser.add_argument('-i', dest='informative', type=int, default=5, help='number of most informative features to show')

    args = parser.parse_args()

    # Run the test
    predictions, metrics, informative = test(args.test_file, args.classifier)

    # Print each prediction
    if args.verbose:
        for title, vector, true_label, predicted_label in predictions:
            if true_label == predicted_label:
                color = 'green'
            else:
                color = 'red'
            print(colored("{} - Actual: {} | Predicted: {}".format(title, true_label, predicted_label), color))


    # Print the metrics
    acc, pre, rec, f1 = metrics
    print("\nMetrics:\n--------")
    print("Accuracy: {} | Precision: {} | Recall: {} | F1: {}".format(round(acc, 4), round(pre, 4), round(rec, 4), round(f1, 4)))

    # Print informative features
    print("\nMost Informative Features:\n--------------------------")
    for feature, _ in informative[0:args.informative]:
        print(feature)
