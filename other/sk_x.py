import csv
from pathlib import Path, PureWindowsPath

gestures = ['RA: move, up', 'RA: move, down', 'LA: move, up', 'LA: move, down', 'head: rotate;', 'body: rotate', 'body: still']

l_to_a = {'RA: move, up': 0,
                'RA: move, down': 1,
                'LA: move, up': 2,
                'LA: move, down': 3,
                'head: rotate;': 4,
                'body: rotate': 5,
                'body: still': 6}

def is_valid_pair(llabel, label):
    l1 = llabel.strip(';')
    l1_list = l1.split('; ')
    l2 = label.strip(';')
    l2_list = l2.split('; ')

    pair = []
    for g1 in l1_list:
        if g1 in gestures:
            pair.append(g1)
            break
            
    for g2 in l2_list:
        if g2 in gestures:
            pair.append(g2)
            break

    if len(pair) == 2:
        return pair
    else:
        return []

def read_master_file(filename):
    with open(filename) as labels:
        csvreader = csv.reader(labels, delimiter='\t')

        last_row = []
        
        for row in csvreader:
            path_to_file = row[2]

            if path_to_file == 'File Name':
                continue

            if not last_row:
                last_row = row
                continue

            lstart, lend, llabel = int(last_row[8]), int(last_row[9]), last_row[10]
            start, end, label = int(row[8]), int(row[9]), row[10]
                       
            gpair = is_valid_pair(last_row[10], row[10])

            if not not gpair:
                if start >= lend:
                    # Clip the appropriate lines in the corresponding skeleton file
                    # Creating filename for the clipped skeleton
                    p = PureWindowsPath(path_to_file)
                    path_to_sk_file = Path('..') / 'z' / p.with_name(p.name.replace('RGB', 'Skeleton', 1).replace('Video', 'Skeleton', 1)).with_suffix('.txt')
                    new_sk_name = path_to_sk_file.name[:-len(path_to_sk_file.suffix)] + '_clipped_' + str(last_row[8]) + '_' + str(end)
                    path_to_new_sk_file = path_to_sk_file.with_name(new_sk_name).with_suffix('.tsv')
                
                    f = path_to_new_sk_file.open('w')

                    with path_to_sk_file.open('r') as sk:
                        cr = csv.reader(sk)
                        i=0
                        for line in cr:
                            if i < lstart+1:

                                i+=1
                                continue

                            elif i < lend+1:

                                f.write('\t'.join(line) + '\t' + str(l_to_a[gpair[0]]) + '\n')
                                i+=1
                                
                            elif i < end+1:

                                f.write('\t'.join(line) + '\t' + str(l_to_a[gpair[1]]) + '\n')
                                i+=1
                                
                            else:

                                f.close()
                                break
            last_row = row
