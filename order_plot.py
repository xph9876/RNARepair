#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
from scipy.stats import spearmanr

# read freqs from input csv file
def generate_data(fra, frb):
    data = []
    for flag, fr in [[True, fra], [False, frb]]:
        fr.readline()
        for l in fr:
            ws = l.rstrip().split('\t')
            if len(ws) < 8:
                continue
            label = ws[0]
            if flag:
                x = int(ws[3])
                y = int(ws[6])
            else:
                x = int(ws[6])
                y = int(ws[3])
            data.append([x,y,label])
    return data


# add order to the data
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


# add color to data
def add_color(data, t):
    c1 = 'blue'
    c2 = 'red'
    out = {c1:[], c2:[]}
    for l in data:
        if max([l[0], l[1]]) < t:
            continue
        if 0 < min([l[0], l[1]]) < t:
            out[c2].append(l)
        elif min([l[0], l[1]]) >= t:
            out[c1].append(l)
    return out



def main():
    parser = argparse.ArgumentParser(description='Get rate plot for sequece with order in file1 vs order in file2')
    parser.add_argument('file1', type=argparse.FileType('r'), help='Preference file 1 in tsv format')
    parser.add_argument('file2', type=argparse.FileType('r'), help='Preference file 2 in tsv format')
    parser.add_argument('-t', type=int, default=1, help='Mininum threshold for read counts (1)')
    parser.add_argument('-o', default='qq.png', help='Output plot name')
    args = parser.parse_args()

    # read order
    data_raw = generate_data(args.file1, args.file2)

    # add order
    data_raw = add_order(data_raw)

    # add color
    data = add_color(data_raw, args.t)

    # plot
    fig, _ = plt.subplots(figsize=(16,16), dpi=100)
    for k,v in data.items():
        # points
        xs = [x[3] for x in v]
        ys = [x[4] for x in v]
        plt.plot(xs, ys, 'o', color=k)

        # label
        for _,_,l,x,y in v:
            plt.annotate(l, (x,y), textcoords="offset points", xytext=(2,-8), fontsize=6)
        name1 = args.file1.name.split('/')[-1].split('.')[0].split('_')[1]
        name2 = args.file2.name.split('/')[-1].split('.')[0].split('_')[1]

    # all points
    xs = []
    ys = []
    for v in data.values():
        xs += [x[3] for x in v]
        ys += [x[4] for x in v]

    # parameters
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

