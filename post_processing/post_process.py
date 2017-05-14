import csv, html
from langdetect import detect
import sys
from csv import DictWriter

with open(sys.argv[1]) as source, open(sys.argv[2], 'w+') as output:
    writer = DictWriter(output, fieldnames=['uploader','id','title','views','age' ])
    writer.writeheader()
    lines = open("videos_raw_all.csv")
    reader = csv.reader(lines)
    for line in reader:
        #set each title to be html parsed.
        line[2] = html.unescape(line[2])
        try :

            if  detect(line[2])== 'en':
                print(line)
                writer.writerow({'uploader' : line[0],'id': line[1],
                'title': line[2],'views': line[3],'age': line[4]})
            else:
                print("Incorrect language detected")
        except:
            continue
