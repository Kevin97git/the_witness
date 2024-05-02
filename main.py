from random import choice, choices, randint, shuffle, seed
from copy import copy
from functools import cmp_to_key
from itertools import groupby
from sys import _getframe
from colorama import Fore, init
import pprint
init(True)

from paint import point, line, vec2, set_a, loop, square, main_draw, grid, shapes, shape, once, all_shape, shape_length_minimum
from config_save_error import raise_error

# config
A_MAX = 8
A_MIN = 5
# Return random integer in range [a, b).
def _rand(a: int, b: int): return randint(a, b-1)
def _rand_bool(a:int, b:int): return 0 in choices([i for i in range(b)], k=a)

#debug
def debug_print_all_line():
    for k in line.all():
        if line.all()[k].exist:
            print(k)
def debug_flag():
    print('flag')


probabilities = {}
# probabilities include const
LPN = 'line_passed_number: '
PI = 'part_index: '
SU = Fore.RED+'shape_unrotatable: '+Fore.RESET
SR = Fore.RED+'shape_rotatabele: '+Fore.RESET # isn't rotated yet

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
def list_compare(x:square, y:square):
    if x.pos.y > y.pos.y: return 1
    elif x.pos.y < y.pos.y: return -1
    else:
        if x.pos.x > y.pos.x: return 1
        else: return -1
def destribute(l1:list, l2:list):
    return [l1+[e] for e in l2]
# region
# def _match(g, prefix=[]):
#     on = g.one_num()
#     sub_sub_p = []
#     for _s in shapes:
#         for rt in range(1 if shape.rotate_the_same(_s) else 4):
#             if sum([sum(i) for i in _s]) > on: continue
#             me = g.match_prefix(shape(_s, rt), prefix)
#             sub_sub_p += me
#             for sme in me:
#                 sub_sub_p += _match(sme[-1][2], prefix=[sme])
#     return sub_sub_p

# def _match(g, prefix=[]):
#     on = g.one_num()
#     sub_sub_p = []
#     for _s in shapes:
#         for rt in range(1 if shape.rotate_the_same(_s) else 4):
#             if sum([sum(i) for i in _s]) > on: continue
#             me = g.match_prefix(shape(_s, rt), prefix)
#             sub_sub_p += me
#     if sub_sub_p == []: return []
#     last = choice(sub_sub_p)
#     sub_sub_p = _match(last[-1][2], prefix=last)
#     return sub_sub_p

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
#     print(len(prefix))
#     while res == [] and len(sub_sub_p) != 0:
#         ind = randint(0, len(sub_sub_p )-1)
#         res = _match(sub_sub_p[ind][-1][2], sub_sub_p[ind])
#         sub_sub_p.pop(ind)
#     return res
# endregion

match_item_type = tuple[shape, vec2, grid]
match_end_type  = list [match_item_type]
shape_prob_type = tuple[shape, vec2]
# (match end: have the same shape, prob, len(match_end))
state_item_type = tuple[list[match_item_type], list[shape_prob_type], int]

def _remove(l:list, item) -> list:
    l.remove(item)
    return l
# get a state-like object to be added into state
def _match(g:grid, 
           prob:list[shape_prob_type], 
           prefix:list = [],
           length:int  = 0
    )->list[state_item_type]: 
    print('_match g:', g, 'prob:', prob if len(prob) < 8 else len(prob), 'len_prefix:', len(prefix), 'length:', length)
    res: list[state_item_type] = []
    # foreach probabilities in order to match by
    for s in prob:
        me, rprob = g.match_prefix(s, prefix=prefix)
        # rprob: all probabilities for matching g
        if me == []: continue
        res += [(mee, _remove(rprob, s), length) for mee in me if rprob != [s]] # delete matched
    shuffle(res)
    return res

def match(g:grid):
    # [
    #  (what list we're foreach-ing: [MET, ...], 
    #   what shape may be matched,
    #   length)]
    state: list[state_item_type] = []
    prob : list[shape_prob_type] = []
    maximum = []
    maximum_len = 0
    # init prob
    mel: list[match_item_type] = []
    for s in all_shape():
        # me: only one shape
        me, sprob = g.match(s)
        prob += sprob
        mel += me
    if mel == []: print('kinda interesting.'); return []
    # length equals to 1
    maximum = choice(mel)
    maximum_len = 1
    for e in mel:
        tmp = copy(prob); tmp.remove((e[-1][0], e[-1][1]))
        state.append((e, tmp, 1))
    print('prob init.\nloop begins')
    
    while True:
        state_now = state[-1]
        state.pop()
        prob = state_now[1]       # what the grid may include
        if prob == []:
            assert False
            print('prob == [], state:', state if len(state) < 8 else len(state))
            state.pop()
            continue
        now  = state_now[0][0][2] # what to match
        res  = _match(now, prob, prefix=state_now[0], length=state_now[2]+1)
        if res == []: # match nothing
            print('match nothing')
            # state.pop()
            if state == []: print('match return max:', maximum); return maximum
            continue
        else:
            print('-----match sth-----')
            if res[-1][2] >= shape_length_minimum:
                print('match return:', res)
                return res
            if res[-1][2] > maximum_len:
                maximum_len = res[-1][2]
                maximum = res[-1]
            state += res

def _sub_pro_eq(a, b):
    if a == [] or b == []:
        return False
    a_ = a[-1][2]
    b_ = b[-1][2]
    if a[-1][2] != b[-1][2]:
        return False
    # for _a in a:
    #     for _b in b:
    #         if _a[0] == _b[0]:
    #             break
    #     else:
    #         return False
    print('eq')
    return True
    

def reset(seed1, seed2):
    global a
    # rand
    seed(seed1 ^ seed2)
    a = randint(A_MIN, A_MAX)
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
        n = s.near_samep()
        n.append(s)
        done = [s]
        while len(n) != len(done):
            i = 0
            for i in range(len(n)):
                if not n[i] in done: break
            done.append(n[i])
            n+=n[i].near_samep(); n = list(set(n))
            i = 0
        for e in n:
            cpy_asv.remove(e)
        n.sort(key=cmp_to_key(list_compare))
        parts.append(n)
    
    # add probabilities: PI
    for ind, p in enumerate(parts):
        print('new_part')
        for e in p:
            if ind <= 5:
                probabilities[e.pos].append((PI, ind))
        g = grid(p)
        sub_pro = match(g)

        # region
        # done = [[]]
        # sub_pro = [[]]
        # for _shape in shapes:
        #     # shape vec2 grid
        #     for i in range(1 if shape.rotate_the_same(_shape) else 4):
        #         se = g.match(shape(_shape, i))
        #         if se != []:
        #             sub_pro += [[sse] for sse in se]

        # while len(done) != len(sub_pro):
        #     print('add_sub_pro')
        #     print('lendone', len(done))
        #     print('lensub', len(sub_pro))
        #     i = 0
        #     for i in range(len(sub_pro)):
        #         if not sub_pro[i] in done: break
        #     done.append(sub_pro[i])
        #     g = sub_pro[i][-1][2]
        #     on = g.one_num()
        #     for _shape in shapes:
        #         if sum([sum(i) for i in _shape]) > on:
        #             print('jump')
        #             continue
        #         for i in range(4):
        #             se = g.match(shape(_shape, i))
        #             if se != []:
        #                 for sse in se:
        #                     for d in sub_pro:
        #                         if _sub_pro_eq(d, [sse]):
        #                             break
        #                     else:
        #                         sub_pro.append(sub_pro[i] + [sse])
            

            # print(sub_pro)
            # print('lendone', len(done))
            # print('before clear:', len(sub_pro))


            # while not(last == len(sub_pro)-1 and last_ == len(sub_pro)-1):
            #     for ind, i in enumerate(sub_pro[last:]):
            #         for ind_, j in enumerate(sub_pro[max(last_, ind+1):]):
            #             if i == j:
            #                 if ind == ind_:
            #                     continue
            #                 print('catch')
            #                 sub_pro.pop(ind)
            #                 last = ind
            #                 last_ = ind_
            #                 break
            #             if _sub_pro_eq(i, j): 
            #                 sub_pro.pop(ind)
            #                 last = ind
            #                 last_ = ind_
            #                 break
            #         else: continue
            #         break

            # i = 0
            # while i < len(sub_pro):
            #     j = i+1
            #     i_ = sub_pro[i]
            #     while j < len(sub_pro):
            #         j_ = sub_pro[j]
            #         if _sub_pro_eq(i_, j_):
            #             sub_pro.pop(j)
            #             print('pop')
            #         j += 1
            #     i += 1

            # print('lendone', len(done))
            # print('end:', len(sub_pro))

            # xxx = [repr(i[-1][2]) if len(i) > 0 else '0' for i in sub_pro]
            # print(xxx)
            # if len(list(set(xxx))) != len(xxx):
            #     print('xxx')
        # endregion
        # TODO
        if sub_pro != []:
            print(sub_pro)
            tmp = []
            for i in sub_pro:
                _once = once(i[:2])
                tmp.append((SU, _once))
                tmp.append((SR, _once))
                
            for squ in p:
                probabilities[squ.pos] += tmp

    # _print = print
    # print = pprint.pprint
    print(parts)
    # print(str(probabilities))
    for k in probabilities:
        print(k, ':[', sep='', end='\n    ')
        for t in probabilities[k]:
            print('(', end='')
            for o in t:
                print(o, end=',')
            print('),\n    ', end='')
        print('],')
    # print = _print
    for y in range(a):
        string = ''
        for x in range(a):
            for ind, sl in enumerate(parts):
                if square(vec2(x, y)) in sl:
                    string += str(ind)
        print(' '.join(string))
    loop()
    # debug_print_all_line()

reset(1, 361886424832)