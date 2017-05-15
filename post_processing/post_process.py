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
        try :

            if  detect(line[2])== 'en' and line[4].split()[1] not in set(["hour", "day"]):
                print(line)
                writer.writerow({'uploader' : line[0],'id': line[1],
                'title': line[2],'views': line[3],'age': line[4]})

            else:
                print("Incorrect language detected or too early")
        except:
            continue
