import matplotlib.pyplot as plt
import numpy as np

acc_lr = [39.37, 50.44, 47.53, 42.93]
acc_lr_hmm = [40.60, 52.73, 47.30, 43.70]

fig, ax = plt.subplots()
width = 0.25

indices = np.arange(1,5)

ax.set_xlabel('Methods')
ax.set_ylabel('Accuracy')

ax.set_title('Linear Regression with and w/o HMM')

r1 = ax.bar(indices - width, acc_lr, width, color='b')
r2 = ax.bar(indices, acc_lr_hmm, width, color='r')

ax.set_xticks(indices)
ax.set_xticklabels(('Raw', 'Frame+Diff', 'Diff', 'Angles'))

ax.legend((r1[0], r2[0]), ('w/o HMM', 'w/ HMM'))
plt.show()
