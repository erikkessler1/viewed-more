import argparse
from csv import DictWriter, DictReader

""" Tool for tagging videos based on a threshold.

For a given threshold, T, marks all videos with a SD above +T 'GOOD'
and all vidos below -T with 'BAD'.

Usage:
  python tagger.py -t [T] <input_file> <output_file>

"""

# Arguments
parser = argparse.ArgumentParser(description='Tag video titles using a given threshold.')
parser.add_argument('input', metavar='in', help='input file')
parser.add_argument('output', metavar='out', help='output file')
parser.add_argument('-t', type=float, required=True, help='threshhold')

args = parser.parse_args()

with open(args.input) as source, open(args.output, 'w+') as output:
    writer = DictWriter(output, fieldnames=['title', 'tag'])
    writer.writeheader()

    # Counts for stats
    tagged_count = 0
    below_count = 0
    good_count = 0
    bad_count = 0

    # Iterate through each video
    for video in DictReader(source):
        sd_from_mean = float(video["sds"])
        distance_from_mean = abs(sd_from_mean)

        if distance_from_mean >= args.t:
            if sd_from_mean > 0:
                tag = 'GOOD'
                good_count += 1
            else:
                tag = 'BAD'
                bad_count += 1
                
            writer.writerow({'title': video["title"], 'tag': tag})
            tagged_count += 1
        else:
            below_count += 1

    print("{} tagged | {} below | {} GOOD | {} BAD".format(tagged_count, below_count, good_count, bad_count))

