import os
from pathlib import Path
import fnmatch
import Skeleton
    
data_dir = Path('..') / 'z'
clips = []

# Store Path objects pointing to clipped skeletons
for root, dirs, files in os.walk(str(data_dir)):
    clips += [ Path(root) / f for f in fnmatch.filter(files, '*clipped*tsv') ]

for c in clips:
    s = Skeleton(str(c))
    s.load(skipheader=False)
    # Need to do some proceesing on skeleton data here
    s.normalize('spine-base')
    s.save()
