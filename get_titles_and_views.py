import sys
import json
import re
from csv import DictWriter
from urllib import request

""" A tool for getting video titles and view counts for uploaders.

Take an input list of YouTube uploader ids and map it to a csv file
where each row is a video with the uploader, title, and view count.


Usage:
  python get_titles_and_views.py <input_file> <output_filename>

"""

def get_video_info(html, index):
    """ Extracts the video title and view count at given index in an html document.

    Args:
      html (string): The html document to extract info from.
      index (int): Location in the document where the video infomation is located.
    Returns:
      (string, int): A tuple of the video title and view count.

    """
    starttitle = html.index("title=", index)
    endtitle = html.index('"', starttitle + 7)
    title = html[starttitle + 7:endtitle]
    
    li_index = html.index("<li>", endtitle)
    views = int(html[li_index+4:html.index(" ", li_index)].replace(',',''))
    
    return (title, views)
    
def grabYoutubers():
    #jsonfile = open('exportUploaders.json')
    import urllib.request
    import html.parser as htmlparser
    parser = htmlparser.HTMLParser()

    vidstatsfront = "https://vidstatsx.com/youtube-top-"
    vidstatsback = "-most-subscribed-channels"
    topx = [200, 500, 750, 1000, 1250, 1500, 1750, 2000]

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}


    youtube_ids= []

    for x in topx:
        link = vidstatsfront + str(x) + vidstatsback
        #grab url
        request=urllib.request.Request(link,None,headers)
        topvideos = urllib.request.urlopen(request)
        page = topvideos.read().decode("utf-8")
        table_index = page.index('table id="youtube-top-')
        end_table = page.index("</table>", table_index)
        try:
            link_index = page.index("www.youtube.com", table_index)
        except ValueError:
            link_index = None
        while link_index != None and link_index < end_table:
            newlink = page[link_index:page.index('"', link_index)]
            youtube_ids.append(newlink)
            link_index = page.index('www.youtube.com', link_index + 20)

    return youtube_ids
    



    """Fetch the uploader's video page (http://www.youtube.com/user/{uploader}/videos) and 
    extract videos from the html response"""
def grab_videos(uploader):
    """ Get all the title and view counts for all videos on an uploader's page
    Args:
      uploader (string): ID of the uploader.
    Returns:
      [(string, int)]: A list of tuples of title and view count.
    """
    
    videos_url = "http://www.youtube.com/user/" + uploader + "/videos"
    response = request.urlopen(videos_url)
    html = response.read().decode("utf-8")

    content_indicies = [m.start() for m in re.finditer('yt-lockup-content', html)]
    return [get_video_info(html, index) for index in content_indicies]


### Main ###

if len(sys.argv) < 3:
    print("Specify an input file with uploader ids and output filename. Usage:\n\tget_title_and_views.py <input_file> <out_filename>")
    exit()

with open(sys.argv[1]) as uploaders, open(sys.argv[2], 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader', 'title', 'views'])
    writer.writeheader()
    for uploader in uploaders:
        uploader = uploader.strip()
        for title, views in grab_videos(uploader):
            writer.writerow({'uploader': uploader, 'title': title, 'views': views})

    

