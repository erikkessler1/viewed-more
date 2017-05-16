import sys, argparse
from csv import DictReader, DictWriter
from collections import defaultdict
import statistics as stats

""" A tool for finding how many SD away from an uploader's mean
    view count a certain video is.

Takes a CSV file with headers uploader, title, and views and
outputs a CSV file with uploader, title, views, age, uploader_mean, uploader_sd, deviations.

Usage:
  python get_mean_sd.py <input> <output>

"""

def create_video_dict(uploader, mean, sd, video):
    """ Creates a dict with all the infomation for the video.

    Used to create a row in the CSV table.
    """
    id, title, views, age = video
    return {
        'uploader': uploader,
        'id': id,
        'title': title,
        'views': views,
        'age': age,
        'uploader_mean': "{0:.2f}".format(mean),
        'uploader_sd': "{0:.2f}".format(sd),
        'sds': "{0:.2f}".format((views - mean)/sd)
    }

def compute_mean_sd(view_counts):
    return (stats.mean(view_counts), stats.stdev(view_counts))

def create_uploader_dict(reader):
    """ Create map from uploader to videos from the CSV reader.

    Args:
      reader (DictReader): CSV reader with headser for uploader, title, and views
    Returns:
      {string: [(string, string, int, string)]}: Dict from uploader to list of video id, title, views, age tuples.
    """
    uploader_dict = defaultdict(list)
    for row in reader:
        uploader_dict[row["uploader"]].append((row["id"], row["title"], int(row["views"]), row["age"]))
    return uploader_dict

### Main ###

# Arguments
parser = argparse.ArgumentParser(description='Compute how many SD from average each video is.')
parser.add_argument('input', metavar='in', help='input file')
parser.add_argument('output', metavar='out', help='output file')

args = parser.parse_args()

# Compute mean and SD and write a row for each video
with open(args.input) as titles_views, open(args.output, 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader', 'id', 'title', 'views', 'age', 'uploader_mean', 'uploader_sd', 'sds'])
    writer.writeheader()

    # Stats
    uploaders_processed = 0
    videos_written = 0
    
    # Iterate through each uploader
    uploader_dict = create_uploader_dict(DictReader(titles_views))
    for uploader, videos in uploader_dict.items():
        if len(videos) > 5:

            mean, sd = compute_mean_sd([views for _, _, views, _ in videos])

            # Iterate through each video and write a row for it
            for video in videos:
                writer.writerow(create_video_dict(uploader, mean, sd, video))
                videos_written += 1

            uploaders_processed += 1

    print("Operation Complete: {} uploaders processed | {} videos written".format(uploaders_processed, videos_written))
