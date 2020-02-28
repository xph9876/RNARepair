from collections import defaultdict
# get reference sequence
def get_ref(fa):
    fa.readline()
    seq = ''
    for l in fa:
        assert l[0] != '>', f'There should be only one sequence in reference Fasta file {fa.name}!'
        seq += l.rstrip()
    return seq


# check number of mismatch
def check_mismatch(s1,s2,mismatch):
    l = min(len(s1), len(s2))
    for i in range(l):
        if s1[i] != s2[i]:
            mismatch -= 1
            if mismatch < 0:
                return False
    return True


# get middle part
def get_middle_part(ws, ref, capture_start, capture_end, anchor_length, mismatch):
    # get read info
    start = int(ws[3]) - 1
    cigar = ws[5]
    seq = ws[9]
    # extend the head
    seq = '-' * start + seq
    # get anchor pos
    a1_s = capture_start - 1
    a1_e = a1_s + anchor_length
    a2_s = capture_end - anchor_length - 1
    a2_e = a2_s + anchor_length
    # decipher cigar
    curr = start
    cache = ''
    insertions = {}
    for c in cigar:
        if c == 'M':
            curr += int(cache)
            cache = ''
        elif c == 'I':
            num = int(cache)
            insertions[curr] = seq[curr:curr+num]
            seq = seq[:curr] + seq[curr+num:]
            cache = ''
        elif c == 'D':
            num = int(cache)
            seq = seq[:curr] + '-' * num + seq[curr:]
            cache = ''
            curr += num
        else:
            cache += c
    # get ref anchors
    a1 = ref[a1_s:a1_e]
    a2 = ref[a2_s:a2_e]
    # get location of anchor in reads
    mm1 = mismatch
    mm2 = mismatch
    for k,v in insertions.items():
        if a1_s <= k < a1_e:
            mm1 -= len(v)
            if mm1 < 0:
                return None
        if a2_s <=k < a2_e:
            mm2 -= len(v)
            if mm2 < 0:
                return None
    # check mismatch
    if not check_mismatch(a1, seq[a1_s:a1_e], mm1):
        return None
    if not check_mismatch(a2, seq[a2_s:a2_e], mm2):
        return None
    # return middle part
    middle = seq[a1_e:a2_s]
    added = 0
    for k in sorted(insertions.keys()):
        if a1_e <= k < a2_s:
            middle = middle[:k-a1_e+added+1] + v + middle[k-a1_e+added+1:]
    return middle


# remove "-" filling of deletions
def remove_fillings(middles):
    results = defaultdict(int)
    for k,v in middles.items():
        k = k.replace('-','')
        results[k] += v
    return results

# merge all parts with the same sequence to the first alignment
def merge_parts(middles):
    aligns = {}
    out = defaultdict(int)
    for k in sorted(middles.keys(), key=lambda x: middles[x]):
        seq = k.replace('-','')
        if seq not in aligns:
            aligns[seq] = k
        out[aligns[seq]] += middles[k]
    return out


# output middles
def output_middles(middles, fw, index=True):
    assert len(middles) > 0, 'No middle part is captured'
    seqs = sorted(middles.keys(), key = lambda x: -middles[x])
    count = sum(middles.values())
    if index:
        fw.write('Id\tSequence\tCount\tFrequency\n')
        curr = 1
        for s in seqs:
            fw.write(f'{curr}\t{s}\t{middles[s]}\t{middles[s]/count}\n')
            curr += 1
    else:
        fw.write('Sequence\tCount\tFrequency\n')
        for s in seqs:
            fw.write(f'{s}\t{middles[s]}\t{middles[s]/count}\n')
