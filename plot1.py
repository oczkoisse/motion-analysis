import matplotlib.pyplot as plt
import numpy as np

acc_ls = [37.52, 51.83, 46.07, 40.88]
acc_ls_hmm = [38.51, 54.18, 48.86, 41.75]

fig, ax = plt.subplots()
width = 0.25

indices = np.arange(1,5)

ax.set_xlabel('Methods')
ax.set_ylabel('Accuracy')

ax.set_title('Linear SVM with and w/o HMM')

r1 = ax.bar(indices - width, acc_ls, width, color='b')
r2 = ax.bar(indices, acc_ls_hmm, width, color='r')

ax.set_xticks(indices)
ax.set_xticklabels(('Raw', 'Frame+Diff', 'Diff', 'Angles'))

ax.legend((r1[0], r2[0]), ('w/o HMM', 'w/ HMM'))
plt.show()
