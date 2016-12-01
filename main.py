import numpy as np
import os, random
from pathlib import Path
from skeleton import Skeleton
from playlist import Playlist

# Choose a random skeleton file for a given gesture
def choose_random_skeleton(gesture):
    current_dir = Path('.')
    data_dir = current_dir / 'data' / 'clean' / gesture
    return random.choice([str(f) for f in list(data_dir.glob("*.txt")) if f.is_file()])


# Number of samples to be taken from each gesture class
tot_samples = 3

# Taking tot_samples number of samples from both gesture classes
x_files = [ choose_random_skeleton('head nod') for i in range(tot_samples) ]
y_files = [ choose_random_skeleton('arms_move_down(with sound)') for i in range(tot_samples) ]


from dtw import dtw

# Generating a similarity matrix from two list of files with equal length
def gen_sim_matrix(x_files, y_files):

    # Get a combined list of the skeleton files chosen earlier
    combined_files = x_files + y_files

    # Initializing the similarity matrix to be used for final comparison
    s_matrix = np.zeros( len(combined_files) ** 2).reshape(len(combined_files), len(combined_files))

    # Populating the similarity matrix with distance outputs from DTW
    for i, file_i in enumerate(combined_files):
        sk_i = Skeleton(file_i)
        sk_i.load(norm='spine-base')
        
        for j, file_j in enumerate(combined_files):
            sk_j = Skeleton(file_j)
            sk_j.load(norm='spine-base')

            dist, cost, acc, path = dtw(sk_i.data, sk_j.data, dist=lambda a, b: np.linalg.norm(a - b))
            s_matrix[i, j] = dist
    return s_matrix

# Generates list of tuples of similar files skeletons
def gen_sim_files(x_files, y_files, s_matrix):
    sim_files = []
    # Get a combined list of the skeleton files chosen earlier
    combined_files = x_files + y_files
    s_matrix_c = np.copy(s_matrix)
    for i in range(len(s_matrix_c)):
        # Need to do this so that 0 entries along the diagonal are not chosen as the minimum
        s_matrix_c[i,i] = float("inf")
        min_index = np.argmin(s_matrix_c[i])
        sim_files += [ (combined_files[i], combined_files[min_index])]
    return sim_files


print("Samples chosen:\n")
for i in x_files + y_files:
    print(i)

print()

print("Similarity matrix is:\n")
s_matrix = gen_sim_matrix(x_files, y_files)
print(s_matrix)

print()

s_files = gen_sim_files(x_files, y_files, s_matrix)
print("Similar files are:\n")
for i in s_files:
    print(i[0])
    print(i[1])
    print()

# Modifying s_files for use into a playlist
# Writing playlist entries for similar files one after the other
# Trimming '_skeleton.txt' from the end and appending '.avi' suitable for the .pls file        
s_v_files = [ tp[i][:-13]+'.avi' for tp in s_files for i in range(len(tp)) ]

# Writing a pls file
p = Playlist(s_v_files)
p.write('similar.pls')




