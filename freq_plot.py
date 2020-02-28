#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
from collections import defaultdict

# read freqs from input csv file
def generate_data(fra, frb, t):
    c1 = 'blue'
    c2 = 'red'
    data = {c1:[], c2:[]}
    for flag, fr in [[True, fra], [False, frb]]:
        fr.readline()
        for l in fr:
            ws = l.rstrip().split('\t')
            if len(ws) < 8:
                continue
            # must reach threshold in at least one library
            if max([int(ws[3]), int(ws[6])]) < t:
                continue
            # color
            curr = data[c1]
            if min([int(ws[3]), int(ws[6])]) < t:
                curr = data[c2]
            # label
            label = ws[0]
            if flag:
                x = float(ws[4])
                y = float(ws[7])
            else:
                x = float(ws[7])
                y = float(ws[4])
            curr.append((x, y, label))
    return data

def main():
    parser = argparse.ArgumentParser(description='Get rate plot for sequece with frequency in a pair of preference files')
    parser.add_argument('file1', type=argparse.FileType('r'), help='Preference file 1 in tsv format')
    parser.add_argument('file2', type=argparse.FileType('r'), help='Preference file 2 in tsv format')
    parser.add_argument('-t', type=int, default=1, help='Mininum threshold for read counts (1)')
    parser.add_argument('-o', default='freq.png', help='Output plot name')
    args = parser.parse_args()

    # read data
    data = generate_data(args.file1, args.file2, args.t)

    # plot
    fig, ax = plt.subplots(figsize=(16,16), dpi=100)
    for c, values in data.items():
        plt.plot([x[0] for x in values], [x[1] for x in values], 'o', color=c)

    # labels
    for vs in data.values():
        for x,y,l in vs:
            plt.annotate(l, (x,y), textcoords="offset points", xytext=(2,-8), fontsize=6)
    name1 = args.file1.name.split('/')[-1].split('.')[0]
    name2 = args.file2.name.split('/')[-1].split('.')[0]
    plt.xlabel(f'Frequency in {name1}')
    plt.ylabel(f'Frequency in {name2}')
    plt.xscale('log')
    plt.yscale('log')

    # limit
    lim = [min(ax.get_xlim()[0], ax.get_ylim()[0]),\
           max(ax.get_xlim()[1], ax.get_ylim()[1])]
    plt.xlim(lim)
    plt.ylim(lim)
    plt.plot(lim, lim, 'k--')

    # count
    count = 0
    for v in data.values():
        count += len(v)
    fig.suptitle(f'Frequency in the two libraries\n Count = {count}, threshold = {args.t}')
    plt.savefig(args.o)
    print('Done!')

if __name__ == '__main__':
    main()

