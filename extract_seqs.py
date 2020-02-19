#!/usr/bin/env python3

import argparse
import sys
from extractUtils import *
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description='Extract desired middle part of sequence from Sam file')
    parser.add_argument('fa', type=argparse.FileType('r'), help='Reference fasta sequence')
    parser.add_argument('sam', type=argparse.FileType('r'), help='Aligned sam file')
    parser.add_argument('-o', type=argparse.FileType('w'), default=sys.stdout, help='Output to file')
    parser.add_argument('-s', type=int, default=0, help='Start position of desired part (0)')
    parser.add_argument('-e', type=int, default=None, help='End position of desired part (End of the refence sequence)')
    parser.add_argument('-r', action='store_true', help='Show original middle part, do not fill deletion with \"-\"')
    parser.add_argument('-m', action='store_true', help='Merge all middle parts with the same sequence to the first alignment')
    parser.add_argument('--anchor_length', type=int, default=20, help='Length of the both anchors to locate middle sequence (20)')
    parser.add_argument('--max_mismatch', type=int, default=1, help='Maximum mismatch allowed in anchors (1)')
    args = parser.parse_args()

    assert not (args.r and args.m), "Cannot use both -r and -m!"

    # read reference sequence
    ref = get_ref(args.fa)


    # categorize
    middles = defaultdict(int)
    for l in args.sam:
        ws = l.rstrip().split('\t')
        if len(ws) < 9:
            continue
        middle = get_middle_part(ws, ref, args.s, args.e, args.anchor_length, args.max_mismatch)
        if middle != None:
            middles[middle] += 1
    
    # remove gap filling
    if args.r:
        middles = remove_fillings(middles)
    
    # merge same reads
    if args.m:
        middles = merge_parts(middles)

    # output
    output_middles(middles, args.o)
    print('Done!')

if __name__ == '__main__':
    main()

