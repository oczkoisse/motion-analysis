import numpy as np

class Skeleton():
    
    def __init__(self, file_name):
        self.file_name = file_name

    # Pulls up torso skeleton data from a general skeleton file, and normalizes it, if given a valid norm value

    def load(self, norm='none'):
        self.data = np.loadtxt(self.filename, dtype='float', delimiter=',', skiprows=1, usecols=(9, 10, 11, 18, 19, 20, 27, 28, 29, 36, 37, 38, 45, 46, 47, 54, 55, 56, 63, 64, 65, 72, 73, 74, 81, 82, 83, 90, 91, 92, 99, 100, 101, 108, 109, 110, 189, 190, 191))

        self.normalize(norm)

    # Normalizes the data

    def __normalize(self, norm):
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
        
