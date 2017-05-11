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


    from csv import DictWriter

    with open("youtubers.csv", 'w+') as output:
        writer = DictWriter(output, fieldnames=['url'])
        writer.writeheader()
        for id in youtube_ids:
            id = id.strip()

            writer.writerow({'url': id})

    return youtube_ids
