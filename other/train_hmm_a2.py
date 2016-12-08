import os
from pathlib import Path
import fnmatch
from skeleton import Skeleton
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from HMM3 import HMM
from sklearn.metrics import accuracy_score, confusion_matrix

# classifer should be an untrained one, only LinearSVC and LogisticRegression are considered here
def train_test_split_observations(ratio, classifier):

    data_dir = Path('..') / 'z'
    clips = []

    # Store Path objects pointing to clipped skeletons
    for root, dirs, files in os.walk(str(data_dir)):
        clips += [ Path(root) / f for f in fnmatch.filter(files, '*clipped*tsv') ]

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

        y += [ s.data[1:, -1].tolist() ]
        # Keep s.data numpy 2d array for now
        s.data = s.data[:, :-1]

        last_frame = None
        temp_clip = []
        for frame in s.data:
            # Note that frame is numpy array 
            if last_frame != None:
                temp_clip += [ (frame-last_frame).tolist() ]
            last_frame = frame

        X += [ temp_clip ]
        
    classifier.fit([frame for clip in X for frame in clip ], [ label for clip in y for label in clip ])

    for clip in X:
        O += [ classifier.predict(clip).tolist() ]
        
    O_test = []
    X_test = []
    y_test = []

    for c in clips_test:
        s = Skeleton(str(c))
        s.load(skipheader=False, delimiter='\t', extracols=(232,)) 

        #s.normalize('spine-base')

        y_test += [ s.data[1:, -1].tolist() ]
        # Keep s.data numpy 2d array for now
        s.data = s.data[:, :-1]

        last_frame = None
        temp_clip = []
        for frame in s.data:
            # Note that frame is numpy array 
            if last_frame != None:
                temp_clip += [ (frame-last_frame).tolist() ]
            last_frame = frame

        X_test += [ temp_clip ]

    for clip in X_test:
        O_test += [ classifier.predict(clip).tolist() ]

    return (X, y, O, X_test, y_test, O_test)

# Flatten a list of lists
def flatten(list_of_lists):
    return [ e for l in list_of_lists for e in l ]

def get_results():

    classifiers = [ LinearSVC(), LogisticRegression() ]

    print('Beginning Experiments')
    for classifier in classifiers:
        X, y, O, X_t, y_t, O_t = train_test_split_observations(0.7, classifier)
        print('Classifier Accuracy on training data:')
        print(classifier.score(flatten(X), flatten(y)))
        print('Classifier Accuracy on test data:')
        print(classifier.score(flatten(X_t), flatten(y_t)))
        print('Confusion Matrix of classifier:')
        print(confusion_matrix(flatten(y_t), flatten(O_t)))
        
        h = HMM(range(5), range(5))
        h.train(O)
        print('Classifier+HMM Accuracy on training data:')
        print(accuracy_score(flatten(y), flatten(h.viterbiSequenceList(O))))
        print('Classifier+HMM Accuracy on test data:')
        print(accuracy_score(flatten(y_t), flatten(h.viterbiSequenceList(O_t))))
        print('Confusion Matrix of classifier+HMM:')
        print(confusion_matrix(flatten(y_t), flatten(h.viterbiSequenceList(O_t))))
