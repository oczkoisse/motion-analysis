import numpy as np
from pathlib import Path

class Skeleton():
    
    def __init__(self, filename):
        self.filename = filename

    # Pulls up torso skeleton data from a general skeleton file
    # Specifically, the x y z coordinates for the following joints are extracted in this order
    # Shoulder Base | Shoulder Mid | Neck | Head | Shoulder Left | Elbow Left | Wrist Left | Hand Left | Shoulder Right | Elbow Right | Wrist Right | Hand Right | Spine Shoulder
    def load(self, skipheader=True, delimiter=',', extracols=()):
        self.extracols = extracols
        self.data = np.loadtxt(self.filename, dtype='float', delimiter=delimiter, skiprows=1 if skipheader else 0, usecols=(9, 10, 11, 18, 19, 20, 27, 28, 29, 36, 37, 38, 45, 46, 47, 54, 55, 56, 63, 64, 65, 72, 73, 74, 81, 82, 83, 90, 91, 92, 99, 100, 101, 108, 109, 110, 189, 190, 191) + self.extracols)

    # Normalizes the data in place, if given a valid norm value. Valid norm values are 'spine-base'. Invalid value means nothing is done
    # Extra cols are not considered for normalization
    def normalize(self, norm):
        if norm == 'spine-base':
            # Normalizes the data around the mean of spinal base point
            spine = np.zeros(3)
            for i in range(3):
                spine[i] = np.mean(self.data[:, i])
            m, n = self.data.shape
            for i in range(n-len(self.extracols)):
                self.data[:, i] -= spine[i % 3]

        else:
            return

    # Changes ordinary skeleton representation into vector angles instead
    def angularize(self):
        m, n = self.data.shape

        n -= len(self.extracols)

        extras = self.data[:, -len(self.extracols):]
        assert n%3 == 0

        new_data = []
        for i in range(m):
            angular = []
            for j in range(0, n-3, 3):
                for k in range(j+3, n, 3):
                    angular += [ self.data[i][j] - self.data[i][k] ]
                    angular += [ self.data[i][j+1] - self.data[i][k+1] ]
                    angular += [ self.data[i][j+2] - self.data[i][k+2] ]

                    norm = np.linalg.norm([ angular[-3], angular[-2], angular[-1] ])
                    angular[-1] /= norm
                    angular[-2] /= norm
                    angular[-3] /= norm
                    
            new_data += [ np.append(np.array(angular), extras[i]) ]
        self.data = np.array(new_data)
    
    def save(self):
        p = Path(self.filename)
        np.savetxt(str(p)[:-len(p.suffix)]+ '_processed' + '.tsv', np.array(self.data), delimiter='\t')
