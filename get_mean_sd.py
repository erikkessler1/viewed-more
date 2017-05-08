import sys
from csv import DictReader, DictWriter
from collections import defaultdict
from statistics import mean, stdev

""" A tool for finding how many SD away from an uploader's mean 
    view count a certain video is.

Takes a CSV file with headers uploader, title, and views and
outputs a CSV file with uploader, title, views, uploader_mean, uploader_sd, deviations.

Usage:
  python get_mean_sd.py <input> <output>

"""

def create_video_dict(uploader, title, views, mean, sd):
    """ Creates a dict with all the infomation for the video.

    Used to create a row in the CSV table.
    """
    return {
        'uploader': uploader,
        'title': title,
        'views': views,
        'uploader_mean': "{0:.2f}".format(mean),
        'uploader_sd': "{0:.2f}".format(sd),
        'devs': "{0:.2f}".format((views - mean)/sd)
    }

def compute_mean_sd(view_counts):
    return (mean(view_counts), stdev(view_counts))

def create_uploader_dict(reader):
    """ Create map from uploader to videos from the CSV reader.

    Args:
      reader (DictReader): CSV reader with headser for uploader, title, and views
    Returns:
      {string: [(string, int)]}: Dict from uploader to list of video title, views tuples.
    """
    uploader_dict = defaultdict(list)
    for row in reader:
        uploader_dict[row["uploader"]].append((row["title"], int(row["views"])))
    return uploader_dict

### Main ###

if len(sys.argv) < 3:
    print("Specify an input file and output file. Usage:\n\tget_mean_sd.py <input_file> <out_filename>")
    exit()

with open(sys.argv[1]) as titles_views, open(sys.argv[2], 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader', 'title', 'views', 'uploader_mean', 'uploader_sd', 'devs'])
    writer.writeheader()
    
    reader = DictReader(titles_views)    
    uploader_dict = create_uploader_dict(reader)
    for uploader, videos in uploader_dict.items():
        mean, sd = compute_mean_sd([views for title, views in videos])
        for title, views in videos:
            writer.writerow(create_video_dict(uploader, title, views, mean, sd))
