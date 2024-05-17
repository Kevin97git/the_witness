'file: main'
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

'file: test'
# import config_save_error as cse
# cse.raise_error('abc')
# cse.raise_error('def')
# def abc():
#     cse.raise_error('ghi')
# abc()

# from inspect import FrameInfo, currentframe
# from types import FrameType
# import os
# def repr_frame(f: FrameType):
#     return f'file {f.f_code.co_filename}, line {f.f_lineno}, in {f.f_code.co_name}'
# def repr_stack(s: list[FrameType]):
#     return ';'.join([repr_frame(f) for f in get_stack()])
# def get_stack():
#     workdir = os.path.abspath('.')
#     frame = currentframe()
#     res = [frame]
#     while (frame := frame.f_back):
#         if not workdir in frame.f_code.co_filename:
#             break
#         res.append(frame)
#     return res
# def abc():
#     d = 1
#     print( ',\n'.join([repr_frame(f) for f in get_stack()]) )
#     e = 2
# abc()


# from random import choice, choices, randint, shuffle, seed
# from copy import copy
# from functools import cmp_to_key
# from itertools import groupby
# from sys import _getframe
# from time import time
# from paint_classes import point, line, vec2, set_a, loop, square, main_draw, grid, shapes, shape, once, all_shape, shape_length_minimum
# from config_save_error import raise_error
# from typing import Any, Self

# def _rand_bool(a:int, b:int): return 0 in choices([i for i in range(b)], k=a)

# probabilities = {}
# # probabilities include const
# LPN = 'line_passed_number: '
# PI = 'part_index: '
# SU = 'shape_unrotatable: '
# SR = 'shape_rotatabele: ' # isn't rotated yet
# def path_sidesway(l: line):
#     while True:
#         if l.horizonal: return False
#         if not l.exist: return False
#         #left
#         if (
#             (not l.left_obj() is None)
#             and (not l.left_obj().exist)
#             and (not line(l.p1.left_obj(), l.p1).exist)
#             and (not l.p1.left_obj().passed)
#             and (not line(l.p2.left_obj(), l.p2).exist)
#             and (not l.p2.left_obj().passed)
#         ):
#             if _rand_bool(1, 4):
#                 l.left_obj().on
#                 l.off
#                 line(l.p1.left_obj(), l.p1).on
#                 line(l.p2.left_obj(), l.p2).on
#                 continue
#             else: break
#         if (
#             (not l.right_obj() is None)
#             and (not l.right_obj().exist)
#             and (not line(l.p1, l.p1.right_obj()).exist)
#             and (not l.p1.right_obj().passed)
#             and (not line(l.p2, l.p2.right_obj()).exist)
#             and (not l.p2.right_obj().passed)
#         ):
#             if _rand_bool(1, 4):
#                 l.right_obj().on
#                 l.off
#                 line(l.p1, l.p1.right_obj()).on
#                 line(l.p2, l.p2.right_obj()).on
#                 continue
#             else: break
#         return False
# # set_a(4)
# def list_compare(x:square, y:square):
#     if x.pos.y > y.pos.y: return 1
#     elif x.pos.y < y.pos.y: return -1
#     else:
#         if x.pos.x > y.pos.x: return 1
#         else: return -1
# print(_getframe().f_lineno)
# def reset(seed1, seed2):
#     global a
#     # rand
#     seed(seed1 ^ seed2)
#     a = randint(5, 8)
#     set_a(a)
#     square.set_by_a(a)
#     # rand important point
#     point_start   = point(vec2(0, randint(0, a)))
#     point_end     = point(vec2(a, randint(0, a)))
#     turning_point = [ point(vec2(i, randint(0, a))).on for i in range(a) ]
#     if point_start is None or point_end is None or None in turning_point:
#         raise_error('Any of important point is none')
#     point_start.on
#     point_end.on

#     # connect them
#     last = point_start
#     for p in turning_point:
#         if p != last:
#             line.from_to_untidy(p, last)
#         last = p.right_obj()
#         line(p, last).on
#     if last != point_end:
#         line.from_to_untidy(last, point_end)

#     # sidesway
#     for l in copy(list(line.all().values())):
#         path_sidesway(l)

#     # probabilities init here, each of them are list
#     # add probabilities: LPN
#     cpy_asv = copy(list(square.all().values()))
#     for s in cpy_asv:
#         t = s.line_passed
#         probabilities[s.pos] = [] if t == 0 else [(LPN, t)]
    
#     # draw once for debug
#     main_draw()

#     # get parts
#     parts = []
#     while len(cpy_asv) != 0:
#         s:square = cpy_asv[0]
#         # print('cpyasv loop', s)
#         n = s.near_samep()
#         n.append(s)
#         done = [s]
#         while len(n) != len(done):
#             # print('n', len(n))
#             # for i in n:
#             #     print(i)
#             i = 0
#             for i in range(len(n)):
#                 if not n[i] in done: break
#             # else:
#                 # print('errorrrrr')
#             # print('by', n[i])
#             # for e in n[i].near_samep():
#             done.append(n[i])
#             n+=n[i].near_samep(); n = list(set(n))
#             i = 0
#                 # if not e in n: n.append(e)
#         for e in n:
#             cpy_asv.remove(e)
#         n.sort(key=cmp_to_key(list_compare))
#         parts.append(n)
#     return parts
    
# parts = reset(1, 114514)

# # def _match(g, prefix=[]): 
# #     on = g.one_num()
# #     sub_sub_p = []  
# #     # get probabelities with one new shape
# #     for _s in shapes:
# #         for rt in range(1 if shape.rotate_the_same(_s) else 4):
# #             if sum([sum(i) for i in _s]) > on: continue
# #             me = g.match_prefix(shape(_s, rt), prefix)
# #             sub_sub_p += me
# #     if sub_sub_p == []: return []
# #     res = []
# #     # print(len(prefix))
# #     while res == [] and len(sub_sub_p) != 0:
# #         ind = randint(0, len(sub_sub_p )-1)
# #         res = _match(sub_sub_p[ind][-1][2], sub_sub_p[ind])
# #         sub_sub_p.pop(ind)
# #     return res



        
#     # while True:
#     #     res, rprob = _match(g, prob, now)
#     #     if res != [] and rprob != []:
#     #         state.append([rprob, res, -1])
#     #     else:
#     #         state.pop()

#     #     # update state: depth first search
#     #     # state: (probabilities for match, what to match with, index)
#     #     while True:
#     #         state[-1][2] += 1
#     #         if state[-1][2] == len(state[-1][1]):
#     #             state.pop()
#     #             continue
#     #         prob = state[-1][0]
#     #         now = state[-1][1][state[-1][2]]
#     #         break

# for ind, p in enumerate(parts):
#     print('new_part')
#     for e in p:
#         if ind <= 5:
#             probabilities[e.pos].append((PI, ind))
#     g = grid(p)
#     t = time()
#     sub_pro = match(g)
#     print(time()-t)
#     print(sub_pro)

'file: pc'

# def view_vec_sub(a, b):
#     return view_vec(a.x - b.x, a.y - b.y)
    # def n_include(self, what, target):
    #     for e in what:
    #         if target in e: return False
    #     return True
    # def __sub__(self, oth):
    #     return grid.by_l([[(self.l[y][x] - oth[y][x]) for x in range(a)] for y in range(a)])
    # def match_prefix(self, s: shape, prefix:list) -> tuple[list[list[tuple[shape, vec2, Self]]], list[tuple[shape, vec2]]]:
    #     res = []
    #     rprob = []
    #     for y in range(a + 1 - s.height):
    #         for x in range(a + 1 - s.width):
    #             se = self - (s.to_grid(x, y))
    #             if se[se == -1].shape == (0,): 
    #                 res.append(prefix + [(s, vec2(x, y), grid.by_l(se))])
    #                 rprob.append((s, vec2(x, y)))
    #     return (res, rprob)
    # def item(self):
    #     res = []
    #     for y in self.l:
    #         for x in y:
    #             if not x in res: res.append(x)
    #     return res

    # @lru_cache
    # def __ne__(self, other):
    #     return self.__repr__() != repr(other)

    
    # print('get parts before sidesway')
    # log('get parts before sidesway')
    # cpy_asv = copy(list(square.all().values()))
    # print('a:', a)
    # parts = get_parts(squares=cpy_asv)
    # print('print parts', parts)
    # log('print parts')
    # print_parts(parts, a)

    
        # print('new_part')


    
    # print_parts(parts, a)
    # pprint.pprint(probabilities)

    # for k in probabilities:
    #     print(k, ':[', sep='', end='\n    ')
    #     for t in probabilities[k]:
    #         print('(', end='')
    #         for o in t:
    #             print(o, end=',')
    #         print('),\n    ', end='')
    #     print('],')

    
    # for e in probabilities:
    #     for _e in probabilities[e]:
    #         if type(_e) != tuple:
    #             assert False

    
    # def draw(self, surface):
    #     center = p2vpo(self.pos, (-LINE_WIDTH/2, -LINE_WIDTH/2))
    #     gfxdraw.aacircle(surface, center[0], center[1], special_point_radius, line_color['line_must_pass'])
    #     gfxdraw.filled_circle(surface, center[0], center[1], special_point_radius, line_color['line_must_pass'])

    # scale_surface = pygame.surface.Surface((10000, 10000))
# def surface_scale(surface):
    # return pygame.transform.smoothscale(surface, (unit, unit))
# pygame.transform.smoothscale
