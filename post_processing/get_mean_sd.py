import sys
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

def create_video_dict(uploader, vid_id, title, views, age, mean, sd):
    """ Creates a dict with all the infomation for the video.

    Used to create a row in the CSV table.
    """
    return {
        'uploader': uploader,
        'id': vid_id,
        'title': title,
        'views': views,
        'age': age,
        'uploader_mean': "{0:.2f}".format(mean),
        'uploader_sd': "{0:.2f}".format(sd),
        'devs': "{0:.2f}".format((views - mean)/sd)
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

if len(sys.argv) < 3:
    print("Specify an input file and output file. Usage:\n\tget_mean_sd.py <input_file> <out_filename>")
    exit()

with open(sys.argv[1]) as titles_views, open(sys.argv[2], 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader', 'id', 'title', 'views', 'age', 'uploader_mean', 'uploader_sd', 'devs'])
    writer.writeheader()
    
    reader = DictReader(titles_views)    
    uploader_dict = create_uploader_dict(reader)
    for uploader, videos in uploader_dict.items():
        mean, sd = compute_mean_sd([views for _, _, views, _ in videos])
        for vid_id, title, views, age in videos:
            writer.writerow(create_video_dict(uploader, vid_id, title, views, age, mean, sd))
