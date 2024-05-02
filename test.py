from random import choice, choices, randint, shuffle, seed
from copy import copy
from functools import cmp_to_key
from itertools import groupby
from sys import _getframe
from time import time
from paint import point, line, vec2, set_a, loop, square, main_draw, grid, shapes, shape, once, all_shape, shape_length_minimum
from config_save_error import raise_error
from typing import Any, Self

def _rand_bool(a:int, b:int): return 0 in choices([i for i in range(b)], k=a)

probabilities = {}
# probabilities include const
LPN = 'line_passed_number: '
PI = 'part_index: '
SU = 'shape_unrotatable: '
SR = 'shape_rotatabele: ' # isn't rotated yet
def path_sidesway(l: line):
    while True:
        if l.horizonal: return False
        if not l.exist: return False
        #left
        if (
            (not l.left_obj() is None)
            and (not l.left_obj().exist)
            and (not line(l.p1.left_obj(), l.p1).exist)
            and (not l.p1.left_obj().passed)
            and (not line(l.p2.left_obj(), l.p2).exist)
            and (not l.p2.left_obj().passed)
        ):
            if _rand_bool(1, 4):
                l.left_obj().on
                l.off
                line(l.p1.left_obj(), l.p1).on
                line(l.p2.left_obj(), l.p2).on
                continue
            else: break
        if (
            (not l.right_obj() is None)
            and (not l.right_obj().exist)
            and (not line(l.p1, l.p1.right_obj()).exist)
            and (not l.p1.right_obj().passed)
            and (not line(l.p2, l.p2.right_obj()).exist)
            and (not l.p2.right_obj().passed)
        ):
            if _rand_bool(1, 4):
                l.right_obj().on
                l.off
                line(l.p1, l.p1.right_obj()).on
                line(l.p2, l.p2.right_obj()).on
                continue
            else: break
        return False
# set_a(4)
def list_compare(x:square, y:square):
    if x.pos.y > y.pos.y: return 1
    elif x.pos.y < y.pos.y: return -1
    else:
        if x.pos.x > y.pos.x: return 1
        else: return -1
print(_getframe().f_lineno)
def reset(seed1, seed2):
    global a
    # rand
    seed(seed1 ^ seed2)
    a = randint(5, 8)
    set_a(a)
    square.set_by_a(a)
    # rand important point
    point_start   = point(vec2(0, randint(0, a)))
    point_end     = point(vec2(a, randint(0, a)))
    turning_point = [ point(vec2(i, randint(0, a))).on for i in range(a) ]
    if point_start is None or point_end is None or None in turning_point:
        raise_error('Any of important point is none')
    point_start.on
    point_end.on

    # connect them
    last = point_start
    for p in turning_point:
        if p != last:
            line.from_to_untidy(p, last)
        last = p.right_obj()
        line(p, last).on
    if last != point_end:
        line.from_to_untidy(last, point_end)

    # sidesway
    for l in copy(list(line.all().values())):
        path_sidesway(l)

    # probabilities init here, each of them are list
    # add probabilities: LPN
    cpy_asv = copy(list(square.all().values()))
    for s in cpy_asv:
        t = s.line_passed
        probabilities[s.pos] = [] if t == 0 else [(LPN, t)]
    
    # draw once for debug
    main_draw()

    # get parts
    parts = []
    while len(cpy_asv) != 0:
        s:square = cpy_asv[0]
        # print('cpyasv loop', s)
        n = s.near_samep()
        n.append(s)
        done = [s]
        while len(n) != len(done):
            # print('n', len(n))
            # for i in n:
            #     print(i)
            i = 0
            for i in range(len(n)):
                if not n[i] in done: break
            # else:
                # print('errorrrrr')
            # print('by', n[i])
            # for e in n[i].near_samep():
            done.append(n[i])
            n+=n[i].near_samep(); n = list(set(n))
            i = 0
                # if not e in n: n.append(e)
        for e in n:
            cpy_asv.remove(e)
        n.sort(key=cmp_to_key(list_compare))
        parts.append(n)
    return parts
    
parts = reset(1, 114514)

# def _match(g, prefix=[]): 
#     on = g.one_num()
#     sub_sub_p = []  
#     # get probabelities with one new shape
#     for _s in shapes:
#         for rt in range(1 if shape.rotate_the_same(_s) else 4):
#             if sum([sum(i) for i in _s]) > on: continue
#             me = g.match_prefix(shape(_s, rt), prefix)
#             sub_sub_p += me
#     if sub_sub_p == []: return []
#     res = []
#     # print(len(prefix))
#     while res == [] and len(sub_sub_p) != 0:
#         ind = randint(0, len(sub_sub_p )-1)
#         res = _match(sub_sub_p[ind][-1][2], sub_sub_p[ind])
#         sub_sub_p.pop(ind)
#     return res



        
    # while True:
    #     res, rprob = _match(g, prob, now)
    #     if res != [] and rprob != []:
    #         state.append([rprob, res, -1])
    #     else:
    #         state.pop()

    #     # update state: depth first search
    #     # state: (probabilities for match, what to match with, index)
    #     while True:
    #         state[-1][2] += 1
    #         if state[-1][2] == len(state[-1][1]):
    #             state.pop()
    #             continue
    #         prob = state[-1][0]
    #         now = state[-1][1][state[-1][2]]
    #         break

for ind, p in enumerate(parts):
    print('new_part')
    for e in p:
        if ind <= 5:
            probabilities[e.pos].append((PI, ind))
    g = grid(p)
    t = time()
    sub_pro = match(g)
    print(time()-t)
    print(sub_pro)