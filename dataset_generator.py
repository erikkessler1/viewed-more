import csv
import wget
from collections import defaultdict

with open('kdd12.dataset.csv') as f:
    reader = csv.DictReader(f)
    ids = set([(row['video_id'], row['cloneset_id'])for row in reader])
    print(len(ids))
    cloneset = defaultdict(list)
    for video_id, clone_id in ids:
        cloneset[int(clone_id)].append(video_id)


    cloneset = sorted(cloneset.items())[:1]
    print(cloneset)
filename = wget.download("https://www.youtube.com/watch?v=Vgs0hiJ3E7A", out="doggo")
print(filename)

# watch-view-count".*>(.*) views
# eow-title.*>(.*)</span
# yt-subscriber-count.*>(.*)</span
# eow-description" class="" >(.*)</p>
