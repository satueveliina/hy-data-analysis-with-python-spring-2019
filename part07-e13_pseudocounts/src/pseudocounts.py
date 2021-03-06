#!/usr/bin/env python3

import sys
from collections import defaultdict
import numpy as np
from pprint import PrettyPrinter

NUCLEOTIDES = ['A', 'T', 'G', 'C']
#assign prob 0.25 to each nucleotide when preceding kmer not found:
MISSING_KMER_PROB = dict(zip(NUCLEOTIDES, [1/len(NUCLEOTIDES)]*len(NUCLEOTIDES)))

def all_kmers(k):
    """A generator that can be used to iterate through all k-mers.
Usage: for kmer in all_kmers(k):
           do_something(kmer)
"""
    if k==0:
        yield ""
    else:
        nucs= "".join(NUCLEOTIDES)
        v=[0]*k
        v[-1]=-1
        limit=pow(4, k)
        for i in range(limit):
            i=k-1
            while v[i] == 3:
                v[i] = 0
                i -= 1
            v[i] += 1
            yield "".join([ nucs[x] for x in v ])

def kmers_in_str(string, k):
    idx = 0
    while idx < len(string) - k:
        kmer = string[idx:idx+k]
        next_n = string[idx+k]
        idx += 1
        yield (kmer, next_n)

def context_list(s, k):
    kmers = defaultdict(str)
    for kmer, next_n in kmers_in_str(s, k):
        kmers[kmer] = kmers[kmer] + next_n
    return dict(kmers)

def get_pseudo_probs(context):
    pseudo_total = len(context) + len(NUCLEOTIDES)
    return {str(nuc): (context.count(nuc) + 1)/pseudo_total for nuc in NUCLEOTIDES}

def context_probabilities(s, k):
    contexts = dict(context_list(s, k))
    kmers = {}
    if(k == 0):
        return get_pseudo_probs(s)
    for kmer in all_kmers(k):
        if(kmer in contexts):
            kmers[kmer] = get_pseudo_probs(contexts[kmer])
        else:
            kmers[kmer] = MISSING_KMER_PROB
    return kmers

if __name__ == '__main__':
    if len(sys.argv) > 1:         # Were command line parameters given?
        s = sys.argv[1]           # First command line parameter is the input string
        try:
            k=int(sys.argv[2])    # Second command line parameter is the context length
        except IndexError:
            k=2
        d=context_probabilities(s, k)
        print(d)
    else:
        s="ATGATATCATCGACGATGTAG"
        pp = PrettyPrinter()
        print("K=2:")
        pp.pprint(context_probabilities("ATGATATCATCGACGATGTAG", 2))
        print("K=0:")
        pp.pprint(context_probabilities("ATGATATCATCGACGATGTAG", 0))

