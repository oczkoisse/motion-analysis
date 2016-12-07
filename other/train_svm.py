import os
from pathlib import Path
import fnmatch
from skeleton import Skeleton
import numpy as np
from sklearn.svm import LinearSVC

data_dir = Path('..') / 'z'
clips = []

# Store Path objects pointing to clipped skeletons
for root, dirs, files in os.walk(str(data_dir)):
    clips += [ Path(root) / f for f in fnmatch.filter(files, '*clipped*tsv') ]


# Random split into training and test data
np.random.shuffle(clips)
split_pt = int(0.8 * len(clips))
clips_train = clips[:split_pt]
clips_test = clips[split_pt:]

X = []
y = []

for c in clips_train:
    s = Skeleton(str(c))
    s.load(skipheader=False, delimiter='\t', extracols=(232,)) 
    #s.normalize('spine-base')
    X += s.data[:,:-1].tolist()
    y += s.data[:,-1].tolist()

X_test = []
y_test = []

for c in clips_test:
    s = Skeleton(str(c))
    s.load(skipheader=False, delimiter='\t', extracols=(232,))
    X_test += s.data[:, :-1].tolist()
    y_test += s.data[:, -1].tolist()

#svm = LinearSVC()
#svm.fit(X,y)
#print(svm.score(X, y))

