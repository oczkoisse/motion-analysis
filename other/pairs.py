import csv
import operator

with open('Labels.tsv') as labels:
    csvreader = csv.reader(labels, delimiter='\t')
    pairs = {}
    last_labels = []
    for row in csvreader:
        filename = row[2]
        start, end, label = row[8:11]
        label = label.strip(';')
        indi_labels = label.split('; ')
        # If we are at first line, do nothing
        if filename == 'File Name':
            continue
        # If we don't have a label to compare to yet, store it for the next time
        elif not last_labels:
            last_labels = indi_labels
        else:
            cur_labels = indi_labels
            for ll in last_labels:
                for lc in cur_labels:
                    pair = ll + ' -> ' + lc
                    if pair in pairs:
                        pairs[pair] += 1
                    else:
                        pairs[pair] = 1
            last_labels = cur_labels

    sorted_labels_pairs = sorted(pairs.items(), key=operator.itemgetter(1))
    sorted_labels_pairs.reverse()
    
    for i in sorted_labels_pairs[:50]:
        print(i)
