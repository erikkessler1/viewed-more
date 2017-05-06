import numpy
import json
import urllib

#dictionary of usernames, maps to a list of tuples, with title and viewcount.

#for each json:
    #grab the user id
    #query youtube.
    #grab each video title, view count, and

def grabYTViews():
    jsonfile = open('exportUploaders.json')
    import urllib.request
    import html.parser as htmlparser
    parser = htmlparser.HTMLParser()
    


    youtubers = {}

    for line in jsonfile:
        data = json.loads(line)
        uploader = data["uploader"]
        youtubers[uploader] = []

        videos_url = "http://www.youtube.com/user/" + uploader + "/videos"
        response = urllib.request.urlopen(videos_url)
        html = response.read().decode("utf-8")
        try:
            content_index = html.index("yt-lockup-content")
        except ValueError:
            content_index = None

        while content_index != None:

            starttitle = html.index("title=", content_index)
            endtitle = html.index('"', starttitle + 7)
            title = html[starttitle + 7:endtitle]
            li_index = html.index("<li>", endtitle)
            views = html[li_index+4:html.index(" ", li_index)]
            youtubers[uploader].append(tuple([title, views]))

            try:
                content_index = html.index("yt-lockup-content", endtitle)
            except ValueError:
                content_index = None



    return youtubers
