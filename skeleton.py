import numpy as np

class Skeleton():
    
    def __init__(self, filename):
        self.filename = filename

    # Pulls up torso skeleton data from a general skeleton file
    def load(self):
        self.data = np.loadtxt(self.filename, dtype='float', delimiter=',', skiprows=1, usecols=(9, 10, 11, 18, 19, 20, 27, 28, 29, 36, 37, 38, 45, 46, 47, 54, 55, 56, 63, 64, 65, 72, 73, 74, 81, 82, 83, 90, 91, 92, 99, 100, 101, 108, 109, 110, 189, 190, 191))

    # Normalizes the data, if given a valid norm value. Valid norm values are 'spine-base'. Invalid value means nothing is done
    def normalize(self, norm):
        if norm == 'spine-base':
            # Normalizes the data around the mean of spinal base point
            spine = np.zeros(3)
            for i in range(3):
                spine[i] = np.mean(self.data[:, i])
            m, n = self.data.shape
            for i in range(n):
                self.data[:, i] -= spine[i % 3]

        else:
            return
