import sys
import json
import re
from csv import DictWriter
from urllib import request

""" A tool for getting video titles, view counts, and age for uploaders.

Take an input list of YouTube uploader ids and map it to a csv file
where each row is a video with the uploader, title, view count, and age.


Usage:
  python get_titles_and_views.py <input_file> <output_filename>

"""

def get_video_info(html, index):
    """ Extracts the video title and view count at given index in an html document.

    Args:
      html (string): The html document to extract info from.
      index (int): Location in the document where the video infomation is located.
    Returns:
      (string, int, age): A tuple of the video title, view count, and age.

    """
    try:
        starttitle = html.index("title=", index)
        endtitle = html.index('"', starttitle + 7)
        title = html[starttitle + 7:endtitle]

        li_index = html.index("<li>", endtitle)
        views = int(html[li_index+4:html.index(" ", li_index)].replace(',',''))

        li_index = html.index("<li>", li_index + 4)
        age = html[li_index+4:html.index(" ago", li_index)]
    
        return (title, views, age)
    except:
        return None




    """Fetch the uploader's video page (http://www.youtube.com/user/{uploader}/videos) and
    extract videos from the html response"""
def grab_videos(uploader):
    """ Get all the title and view counts for all videos on an uploader's page
    Args:
      uploader (string): ID of the uploader.
    Returns:
      [(string, int, string)]: A list of tuples of title, view count, and age.
    """

    videos_url = "http://www.youtube.com/user/" + uploader + "/videos"
    response = request.urlopen(videos_url)
    html = response.read().decode("utf-8")

    content_indicies = [m.start() for m in re.finditer('yt-lockup-content', html)]
    return filter(None, [get_video_info(html, index) for index in content_indicies])


### Main ###

if len(sys.argv) < 3:
    print("Specify an input file with uploader ids and output filename. Usage:\n\tget_title_and_views.py <input_file> <out_filename>")
    exit()

with open(sys.argv[1]) as uploaders, open(sys.argv[2], 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader', 'title', 'views', 'age'])
    writer.writeheader()

    count = 0
    for uploader in uploaders:
        uploader = uploader.strip()
        for title, views, age in grab_videos(uploader):
            writer.writerow({'uploader': uploader, 'title': title, 'views': views, 'age': age})
        count += 1
        print("{} complete".format(count))
