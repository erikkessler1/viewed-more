import argparse
from train_classifier import generate_feature_vector
from test_classifier import load_classifier
from termcolor import colored

""" Utility that allows a user to test two different titles. 

Usage:
  python viewed_more.py <classifier>

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Which title will be viewed more? Try it!')
    parser.add_argument('classifier', help='file of the classifier')

    args = parser.parse_args()

    print("\nVIEWED MORE\n----------\nWrite two titles and see which one the classifier predicts to be better...\n")
    classifier, features = load_classifier(args.classifier)

    while True:
        title1 = input("Enter a title: ")
        title2 = input("Second title: ")

        title1_vector = generate_feature_vector(title1, features)
        title2_vector = generate_feature_vector(title2, features)
        title1_prob = classifier.prob_classify(title1_vector).prob('GOOD')
        title2_prob = classifier.prob_classify(title2_vector).prob('GOOD')

        if title1_prob > title2_prob:
            winner = title1
        else:
            winner = title2

        print("\nWINNER: " + colored(winner, 'green', attrs=['bold']) + "\n")
