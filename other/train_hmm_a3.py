import os
from pathlib import Path
import fnmatch
from skeleton import Skeleton
import numpy as np
import matplotlib.pyplot as plt

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
        s.angularize()
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
        s.angularize()
        X_test += [ s.data[:, :-1].tolist() ]
        y_test += [ s.data[:, -1].tolist() ]

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
        cm1 = confusion_matrix(flatten(y_t), flatten(O_t))
        plt.figure()
        plot_confusion_matrix(cm1, ['RA: move, up', 'RA: move, down', 'LA: move, up', 'LA: move, down', 'head: nod'])
        

        h = HMM(range(5), range(5))
        h.train(O)
        print('Classifier+HMM Accuracy on training data:')
        print(accuracy_score(flatten(y), flatten(h.viterbiSequenceList(O))))
        print('Classifier+HMM Accuracy on test data:')
        print(accuracy_score(flatten(y_t), flatten(h.viterbiSequenceList(O_t))))
        print('Confusion Matrix of classifier+HMM:')
        cm2 = confusion_matrix(flatten(y_t), flatten(h.viterbiSequenceList(O_t)))
        plt.figure()
        plot_confusion_matrix(cm2, ['RA: move, up', 'RA: move, down', 'LA: move, up', 'LA: move, down', 'head: nod'])
        plt.show()

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
