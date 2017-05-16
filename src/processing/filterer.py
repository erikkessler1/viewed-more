import sys, html, argparse, logging
from csv import DictWriter, DictReader
from polyglot.detect import Detector as LanguageDetector

""" Tool for filtering out titles based on language and age.

Filters out videos based on on langauge (optional) and age.
Videos less than 2 days old are removed, and non-english videos are removed.

Usage:
  python filterer.py [-l] <input_file> <output_file>

"""

# Arguments
parser = argparse.ArgumentParser(description='Filter video files based on age and location.')
parser.add_argument('input', metavar='in', help='input file')
parser.add_argument('output', metavar='out', help='output file')
parser.add_argument('-l', action='store_const', default=False, const=True, help='remove non-english titles')

args = parser.parse_args()

logging.disable(logging.CRITICAL)

# Excludes any videos newer than 2 days
excluded_ages = set(["hour", "hours", "day", "minutes", "minute"])

with open(args.input) as source, open(args.output, 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader', 'id', 'title', 'views', 'age', 'uploader_mean', 'uploader_sd', 'sds'])
    writer.writeheader()

    # Iterate through all the videos
    removed = 0
    written = 0
    for video in DictReader(source):
        video["title"] = html.unescape(video["title"])
        upload_age = video["age"].split()[1]

        # Check that old enough
        if upload_age in excluded_ages:
            removed += 1
            continue

        if args.l:
            language = LanguageDetector(video["title"], quiet=True)

            # Check language is reliable and english
            if not language.reliable or language.language.code != 'en':
                removed += 1
                continue
            
        writer.writerow(video)
        written += 1

    print("Processing Complete: {} written | {} removed".format(written, removed))
