def fullVector(alltitles):
    """Creates a starting dictionary for the bag of words approach"""
    return {word:False for title in alltitles for word in title.split()}

def createVector(title, alltitles):
    """Creates a vector"""
    for word in title:
        alltitles[word] = True
    return alltitles

def NaiveBayes(startingdict):

    allwords = fullVector([title for title in ])





# def containsQorEx(title, alltitles):
#     """if the title contains a question or an exclamation, add it in"""
#     if title.contains("?"):
#         alltitles["ends_q"] = True
#     else:
#         alltitles["ends_q"] = False
#
#     if title.contains("!"):
#         alltitles["ends_ex"] = True
#     else:
#         alltitles["ends_ex"] = False
