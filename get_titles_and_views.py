import numpy
import json
import urllib

#dictionary of usernames, maps to a list of tuples, with title and viewcount.

#for each json:
    #grab the user id
    #query youtube.
    #grab each video title, view count, and

if __name__ == "__main__":
    grabYTViews()

def grabYTViews():
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

    #return youtube_ids

    for url in youtube_ids:
        # uploader = data["uploader"]
        # print(uploader)
        # youtubers[uploader] = []
        #

        videos_url = url + "/videos"
        response = urllib.request.urlopen(videos_url)
        html = response.read().decode("utf-8")
        try:
            content_index = html.index("yt-lockup-content")
        except ValueError:
            content_index = None

        while content_index != None:

            starttitle = html.index("title=", content_index)
            endtitle = html.index('"', starttitle + 7)
            title = parser.unescape(html[starttitle + 7:endtitle])
            li_index = html.index("<li>", endtitle)
            views = html[li_index+4:html.index(" ", li_index)]
            youtubers[uploader].append(tuple([title, views]))


            try:
                content_index = html.index("yt-lockup-content", endtitle)
            except ValueError:
                content_index = None



    return youtubers
