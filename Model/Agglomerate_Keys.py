# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:35:58 2020

@author: j68452
"""

import hashlib as hsh
import random as rd
import copy


rd.seed(0)

Local_Keys_Backup = copy.deepcopy(Key_Conglomerate)

def Distance_Calculator(ptA, ptB):
    dist = []
    center = []
    for ind, x in enumerate(ptA):
        # add something that ignores song length
        dist.append(abs(x - ptB[ind]))
        center.append((x + ptB[ind])/2)
    return sum(dist), center

min_key = [0] * len(ceilings)
max_key = [len(x) for key, x in ceilings.items()]
steps = [x - 1 for x in max_key]
total_iterations = sum(steps)

if 'Key_Conglomerate' in locals():
    # Change tracker to be 1 combinations

    for key, val in Key_Conglomerate.items():
        Key_Conglomerate[key] = [1, val[1]]
    print('completed Setting combinations to 1')

    Combiner = {}
    Centers = {}
    while len(Key_Conglomerate) > 1:
        keys = list(Key_Conglomerate.keys())
        rd.shuffle(keys)
        Key_Conglomerate = {key: Key_Conglomerate[key] for key in keys}
        min_comb = ['','',-1, 0, []]
        key, val = next(iter(Key_Conglomerate.items()))
        for key1, val1 in Key_Conglomerate.items():
            if key != key1:
                dist, center = Distance_Calculator(val[1], val1[1])
                if dist < min_comb[3] or min_comb[2] == -1:
                    pts = max(val[0], val1[0]) + 1
                    min_comb = [key, key1, pts, dist, center]

        if min_comb[0] != '' and min_comb[1] != '':
            print('Combining {} and {}'.format(key, key1))
            N_Key = hsh.md5(min_comb[0].encode('utf-8')+min_comb[1].encode('utf-8'))
            Key_Conglomerate[N_Key.hexdigest()] = [min_comb[2], min_comb[4]]
            Combiner[min_comb[0]] = N_Key.hexdigest()
            Combiner[min_comb[1]] = N_Key.hexdigest()
            Centers[N_Key.hexdigest()] = min_comb[4]
            del Key_Conglomerate[min_comb[0]]
            del Key_Conglomerate[min_comb[1]]

else:
    print("Cannot perform agglomerative clustering without a Key Conglomerate dictionary.")


