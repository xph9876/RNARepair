#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
from collections import defaultdict

# read freqs from input csv file
def generate_freq(fr):
    fr.readline()
    freqs = defaultdict(lambda :(0,0.0))
    for l in fr:
        ws = l.rstrip().split('\t')
        if len(ws) < 2:
            continue
        count = int(ws[1])
        freqs[ws[0]] = (count, float(ws[2]))
    return freqs


# generate preference
def generate_preference(o1, o2):
    preference = {}
    for k, v in o1.items():
        preference[k] = True if v[1]>o2[k][1] else False
    for k, v in o2.items():
        preference[k] = False if v[1]>o1[k][1] else True
    return preference


def main():
    parser = argparse.ArgumentParser(description='Get rate plot for sequece with freq in file1 vs freq in file2')
    parser.add_argument('file1', type=argparse.FileType('r'), help='Tsv file 1')
    parser.add_argument('file2', type=argparse.FileType('r'), help='Tsv file 2')
    parser.add_argument('-o', default='preference', help='Output base name')
    args = parser.parse_args()

    # read freq
    freqs1 = generate_freq(args.file1)
    freqs2 = generate_freq(args.file2)

    # generate points
    preferences = generate_preference(freqs1, freqs2)

    # output
    name1 = args.file1.name.split('/')[-1].split('.')[0]
    name2 = args.file2.name.split('/')[-1].split('.')[0]
    with open(f'{args.o}_{name1}.tsv', 'w') as f1, open(f'{args.o}_{name2}.tsv', 'w') as f2:
        f1.write(f'Sequence\t{name1}_count\t{name1}_freq\t{name2}_count\t{name2}_freq\n')
        f2.write(f'Sequence\t{name2}_count\t{name2}_freq\t{name1}_count\t{name1}_freq\n')
        for k,v in preferences.items():
            if v:
                f1.write(f'{k}\t{freqs1[k][0]}\t{freqs1[k][1]}\t{freqs2[k][0]}\t{freqs2[k][1]}\n')
            else:
                f2.write(f'{k}\t{freqs2[k][0]}\t{freqs2[k][1]}\t{freqs1[k][0]}\t{freqs1[k][1]}\n')
    print('Done!')

if __name__ == '__main__':
    main()

