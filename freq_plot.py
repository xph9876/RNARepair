#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
from collections import defaultdict

# read orders from input csv file
def generate_freq(fr, t):
    fr.readline()
    freqs = defaultdict(float)
    for l in fr:
        ws = l.rstrip().split('\t')
        if len(ws) < 2:
            continue
        count = int(ws[1])
        if count < t:
            return freqs
        freqs[ws[0]] = float(ws[2])
    return freqs


# generate points
def generate_points(o1, o2):
    x = []
    y = []
    for k,v in o1.items():
        x.append(v)
        y.append(o2[k])
    for k,v in o2.items():
        if k not in o1:
            x.append(o1[k])
            y.append(v)
    return x,y


def main():
    parser = argparse.ArgumentParser(description='Get rate plot for sequece with frequency in file1 and file2')
    parser.add_argument('file1', type=argparse.FileType('r'), help='Tsv file 1')
    parser.add_argument('file2', type=argparse.FileType('r'), help='Tsv file 2')
    parser.add_argument('-t', type=int, default=1, help='Mininum threshold for read counts (1)')
    parser.add_argument('-o', default='freq.png', help='Output plot name')
    args = parser.parse_args()

    # read order
    orders1 = generate_freq(args.file1, args.t)
    orders2 = generate_freq(args.file2, args.t)

    # generate points
    xs,ys = generate_points(orders1, orders2)

    # plot
    fig, _ = plt.subplots(figsize=(8,8))
    plt.plot(xs, ys, 'o')

    # label
    name1 = args.file1.name.split('/')[-1].split('.')[0]
    name2 = args.file2.name.split('/')[-1].split('.')[0]
    plt.xlabel(f'Rank in {name1}')
    plt.ylabel(f'Rank in {name2}')
    lim = max(xs + ys)
    plt.xlim([0, lim])
    plt.ylim([0, lim])
    plt.plot([0, lim], [0,lim], 'k--')
    # spearman's correlation
    fig.suptitle(f'Frequency in the two libraries\n Count = {len(xs)}, threshold = {args.t}')
    plt.savefig(args.o)
    print('Done!')

if __name__ == '__main__':
    main()

