import csv
from pathlib import Path

gestures = ['RA: move, up', 'RA: move, down', 'LA: move, up', 'LA: move, down', 'body: still', 'head: rotate;', 'body: rotate']
            
with open('Labels.tsv') as labels:
    csvreader = csv.reader(labels, delimiter='\t')
    # To keep track of a possible pair of gestures
    last_row = []
    for row in csvreader:
        file = row[2]
        # If we are at first line, do nothing
        if file == 'File Name':
            continue
        start, end, label = row[8:11]
        label = label.strip(';')
        # Individual labels, note that there won't be any ;
        indi_labels = label.split('; ')

        # If we don't have the last row, then there is no transition to clip, so go to next row
        if not last_row:
            last_row = row
            continue
        else:
            # If we have some valid gesture in current frame, then ok
            # note that validity is defined as two frames having at least a gesture each from the set of valid gestures
            valid_pair = False
            for i in indi_labels:
                if i in gestures:
                    valid_pair = True
                    break
            # Ensure that the pair is valid and the current frame follows the previous one
            if valid_pair and start >= last_row[9]: # last_row[9] is the end time in previous row
                # Clip the appropriate lines in the corresponding skeleton file
                file_path_components = file.split('\\')
                path_to_sk_file = Path('..') / 'z' / file_path_components[0] / file_path_components[1] / file_path_components[2][:-4] + '.txt'

                f = open( + '_' + str(start) + '_' + str(end) + '_clipped.txt', 'w')
                with open(path_to_sk_file) as sk:
                    i=0
                    for line in sk:
                    if i<start:
                        i+=1
                        continue
                    elif i<end:
                        f.write(line+'\t'+)
                        i+=1
                    else:
                        f.close()
                        break
