#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
from scipy.stats import spearmanr

# read freqs from input csv file
def generate_data(fra, frb, t):
    data = []
    for flag, fr in [[True, fra], [False, frb]]:
        fr.readline()
        for l in fr:
            ws = l.rstrip().split('\t')
            if len(ws) < 8:
                continue
            if min([int(ws[3]), int(ws[6])]) < t:
                continue
            label = ws[0]
            if flag:
                x = float(ws[4])
                y = float(ws[7])
            else:
                x = float(ws[7])
                y = float(ws[4])
            data.append([x,y,label])
    return data


# add order to the data file
def add_order(data):
    # lib1
    data = sorted(data, key = lambda x: -x[0])
    curr = 1
    data[0].append(1)
    for i in range(len(data)-1):
        if data[i][0] == data[i+1][0]:
            data[i+1].append(data[i][-1])
        else:
            data[i+1].append(curr)
        curr += 1
    # lib2
    data.sort(key = lambda x: -x[1])
    curr = 1
    data[0].append(1)
    for i in range(len(data)-1):
        if data[i][1] == data[i+1][1]:
            data[i+1].append(data[i][-1])
        else:
            data[i+1].append(curr)
        curr += 1
    return data



def main():
    parser = argparse.ArgumentParser(description='Get rate plot for sequece with order in file1 vs order in file2')
    parser.add_argument('file1', type=argparse.FileType('r'), help='Preference file 1 in tsv format')
    parser.add_argument('file2', type=argparse.FileType('r'), help='Preference file 2 in tsv format')
    parser.add_argument('-t', type=int, default=1, help='Mininum threshold for read counts (1)')
    parser.add_argument('-o', default='qq.png', help='Output plot name')
    args = parser.parse_args()

    # read order
    data = generate_data(args.file1, args.file2, args.t)

    # add order
    data = add_order(data)

    # points
    xs = [x[3] for x in data]
    ys = [x[4] for x in data]

    # plot
    fig, _ = plt.subplots(figsize=(16,16), dpi=100)
    plt.plot(xs, ys, 'o')

    # label
    for _,_,l,x,y in data:
        plt.annotate(l, (x,y), textcoords="offset points", xytext=(2,-8), fontsize=6)
    name1 = args.file1.name.split('/')[-1].split('.')[0].split('_')[1]
    name2 = args.file2.name.split('/')[-1].split('.')[0].split('_')[1]

    plt.xlabel(f'Order in {name1}')
    plt.ylabel(f'Order in {name2}')
    lim = max(xs + ys)
    plt.xlim([0, lim])
    plt.ylim([0, lim])
    plt.plot([0, lim], [0,lim], 'k--')
    # spearman's correlation
    rho,_ = spearmanr(xs, ys)
    fig.suptitle(f'Order relations in the two libraries\n Count = {len(xs)}, Spearman coef = {rho}, threshold = {args.t}')
    plt.savefig(args.o)
    print('Done!')

if __name__ == '__main__':
    main()

