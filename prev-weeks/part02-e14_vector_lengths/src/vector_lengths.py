#!/usr/bin/env python3

import numpy as np
#import scipy.linalg

def vector_lengths(a):
    np.sum([1])
    return np.sqrt((a**2).sum(axis=1))

def main():
    print(vector_lengths(
        np.array([[ 4,  9, 16],
       [16, 25, 36]])))

if __name__ == "__main__":
    main()
