import os
from pathlib import Path
import fnmatch
from skeleton import Skeleton
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from HMM3 import HMM

data_dir = Path('..') / 'z'
clips = []

# Store Path objects pointing to clipped skeletons
for root, dirs, files in os.walk(str(data_dir)):
    clips += [ Path(root) / f for f in fnmatch.filter(files, '*clipped*tsv') ]


# classifer should be an untrained one, only LinearSVC and LogisticRegression are considered here
def train_test_split_observations(clips, ratio, classifier):
    # Random split into training and test data
    np.random.shuffle(clips)
    split_pt = int(ratio * len(clips))
    clips_train = clips[:split_pt]
    clips_test = clips[split_pt:]

    O = []
    X = []
    y = []

    for c in clips_train:
        s = Skeleton(str(c))
        s.load(skipheader=False, delimiter='\t', extracols=(232,)) 
        #s.normalize('spine-base')
        X += [ s.data[:,:-1].tolist() ]
        y += [ s.data[:,-1].tolist() ]

    classifier.fit([frame for clip in X for frame in clip ], [ label for clip in y for label in clip ])

    for clip in X:
        O += [ classifier.predict(clip).tolist() ]
        
    O_test = []
    X_test = []
    y_test = []

    for c in clips_test:
        s = Skeleton(str(c))
        s.load(skipheader=False, delimiter='\t', extracols=(232,))
        X_test += [ s.data[:, :-1].tolist() ]
        y_test += [ s.data[:, -1].tolist() ]

    for clip in X_test:
        O_test += [ classifier.predict(clip).tolist() ]
        
    return (X, y, O, X_test, y_test, O_test)

