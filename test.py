from time import time, sleep
from functools import cache, lru_cache
import matplotlib.pyplot as plt
import numpy as np
from random import Random
import math
def log_time(func):
    def f(*arg, **kwargs):
        _t = time()
        res = func(*arg, **kwargs)
        if (dt := time() - _t) != 0.0: print(dt)
        return res
    return f
# @cache
# def ways(m, n):
#     if m == 0: return 1
#     if n == 1: return 1
#     return sum([ways(m-this_split_num, n-1) for this_split_num in range(0, m+1)])
# TODO keep this
# TODO keep this
# TODO keep this
# TODO keep this
# TODO keep this
# TODO keep this
# TODO keep this
# TODO keep this
# TODO keep this
@lru_cache(128)
def _ways(m, n):
    num = 0
    todo = [(m, n)]
    print(m, n, end=' ')
    while todo != []:
        m, n = todo[-1]
        todo.pop()
        if m == 0: num += 1;   continue
        if n == 2: num += m+1; continue
        if n == 1: num += 1;   continue
        todo += [(m-this_split_num, n-1) for this_split_num in range(0, m+1)]
    print(num)
    return num
rand = Random()
def split_sequence(rand:Random, seq, num):
    if num == 1: return [seq]
    lseq = len(seq)
    index = [i for i in range(0, lseq+1)]
    ind1 = rand.choices(index, weights=[_ways(lseq-i, num-1) for i in range(lseq+1)])[0]+1
    return [seq[:ind1]] + split_sequence(rand, seq[ind1:], num-1)

def _split_sequence(rand:Random, seq, num):
    res = []
    lseq = len(seq)
    while num != 1:
        index = [i for i in range(0, lseq+1)]
        ind1 = rand.choices(index, weights=[_ways(lseq-i, num-1) for i in range(lseq+1)])[0]+1
        res.append(seq[:ind1])
        seq = seq[ind1:]
        lseq -= ind1
        num -= 1
    res.append(seq)
    return res
print(_ways(30, 5))
print(math.factorial(30+4)/(math.factorial(30)*math.factorial(4)))
# rand.seed(4)
# r = split_sequence(rand, [i for i in range(30)], 5)
# print(r)
# rand.seed(4)
# r = _split_sequence(rand, [i for i in range(30)], 5)
# print(r)
'''
this means
f(0, n) = 1
f(m, 1) = 1
f(m, n) = \sum{m}{i = 0} f(m-i, n-1)
f(m, n) = \sum{m}{i = 0} \sum{m-i}{j = 0} f(m-i-j, n-2)


'''
# print(ways(37, 3)) # res 741
# m = np.arange(0, 120)
# n = np.repeat(5, 120)
# w = []
# for _m, _n in zip(m, n):
#     w.append(ways(_m, _n))
# w = np.array(w)
# plt.plot(m, w)
# plt.show()

'''

def _ways(m, n):
    num = 0
    todo = [(m, n)]
    print(m, n, end=' ')
    while todo != []:
        m, n = todo[-1]
        todo.pop()
        if m == 0: num += 1;   continue
        if n == 2: num += m+1; continue
        if n == 1: num += 1;   continue
        todo += [(m-this_split_num, n-1) for this_split_num in range(0, m+1)]
    return num
def split_sequence(rand:Random, seq, num):
    res = []
    lseq = len(seq)
    while num != 1:
        index = [i for i in range(0, lseq+1)]
        ind1 = rand.choices(index, weights=[_ways(lseq-i, num-1) for i in range(lseq+1)])[0]+1
        res.append(seq[:ind1])
        seq = seq[ind1:]
        lseq -= ind1
        num -= 1
    res.append(seq)
'''