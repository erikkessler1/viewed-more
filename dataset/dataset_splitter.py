import argparse
import random
from csv import DictWriter, DictReader

""" Tool for splitting CSV dataset into train and test files.

For a given training percentage, T, splits into training file with T% and test file with (1-T)%

Usage:
  python dataset_splitter.py -t [T] <input_file> <output_file_base>

"""

# Arguments
parser = argparse.ArgumentParser(description='Split dataset into training and test.')
parser.add_argument('input', metavar='in', help='input file')
parser.add_argument('base', help='output file basename')
parser.add_argument('-t', type=float, required=True, help='Percentage training')

args = parser.parse_args()

print("Spitting into {} train".format(args.t))

with open(args.input) as source, open("{}_train.csv".format(args.base), 'w+') as train, open("{}_test.csv".format(args.base), 'w+') as test:
    reader = DictReader(source)
    
    train_writer = DictWriter(train, fieldnames=reader.fieldnames)
    test_writer = DictWriter(test, fieldnames=reader.fieldnames)
    train_writer.writeheader()
    test_writer.writeheader()

    all = [row for row in reader]

    # Split them
    random.shuffle(all)
    train = all[:int(len(all) * args.t)]
    test = all[int(len(all) * args.t):]

    # Write them
    for row in train:
        train_writer.writerow(row)

    for row in test:
        test_writer.writerow(row)


    
