#!/usr/bin/env python3

import argparse
import sys
import os

# read jobs
def read_jobs(fr):
    jobs = []
    for l in fr:
        ws = l.rstrip('\n').split('\t')
        if len(ws) != 3:
            continue
        jobs.append([ws[0], int(ws[1]), int(ws[2])])
    return jobs


# select desired reads
def select_reads(fr, fw, min_size, max_size):
    # first read
    cache = []
    for i in range(4):
        cache.append(fr.readline())
    line_num = 4
    # iterations
    for l in fr:
        if line_num % 4 == 0:
            if min_size <= len(cache[1].rstrip('\n')) <= max_size:
                fw.write(''.join(cache))
            cache = [l]
        else:
            cache.append(l)
            assert len(cache) <= 4, cache
        line_num += 1
    if min_size <= len(cache[1].rstrip('\n')) <= max_size:
        fw.write(''.join(cache))


def main():
    parser = argparse.ArgumentParser(description='Select reads with desired size')
    parser.add_argument('folder', help='Folder of FASTQ files. Main name should be same with library_name, extension name = fq ')
    parser.add_argument('list', type=argparse.FileType('r'), help='List of libraries. 3 columns. Library_name\tMin_size\tMax_size')
    parser.add_argument('-o', default='selected_reads', help='Output folder name, default = selected_reads')
    args = parser.parse_args()

    # make dir if not exists
    if not os.path.isdir(args.o):
        os.mkdir(args.o)

    # read get jobs
    jobs = read_jobs(args.list)

    # trim
    for lib, min_size, max_size in jobs:
        with open(f'{args.folder}/{lib}.fq', 'r') as fr, open(f'{args.o}/{lib}.fq', 'w') as fw:
            select_reads(fr, fw, min_size, max_size)
        print(f'{lib} finished! output to {fw.name}.')
    print('Done!')


if __name__ == '__main__':
    main()

