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


#debug
# def debug_print_all_line():
#     for k in line.all():
#         if line.all()[k].exist:
#             print(k)
# def debug_flag(): print('flag')


# def destribute(l1:list, l2:list):
#     return [l1+[e] for e in l2]




########################################################################################
'file:pc'
# @property # never cache this!
    # def progress_offset(self):
    #     return tuple_sum(self.draw_progress, 
    #                      self.draw_offset)
    # @property_cache
    # def area(self): return p2vpo(self.pos2) - p2vpo(self.pos1, self.draw_offset)
    # @property_cache
    # def progress_unit(self): return view_vec(0, 1) if self.area[0] == 0 else view_vec(1, 0)
    
'method draw draw progress'

        # if self.draw_progress == 0: 
        #     assert p2vpo(self.pos1, self.draw_offset).to_tuple() == p2vpo(self.pos1, self.progress_offset).to_tuple()
        #     return
        # draw_line(surface, line_color['draw'], 
        #           p2vpo(self.pos1, self.draw_offset).to_tuple(), 
        #           p2vpo(self.pos1, self.progress_offset).to_tuple(),
        #           LINE_WIDTH, self.horizonal)
        # print(self, self.draw_progress, p2vpo(self.pos1, self.draw_offset).to_tuple(), p2vpo(self.pos1, self.progress_offset).to_tuple())

'class line'

    # def set_progress(self, 
    #                  direction:Literal['up']|Literal['down']|Literal['left']|Literal['right'], 
    #                  num) -> Literal[1, -1]|Self:
    #     if self.type == 'line_cannot_pass': return -1
    #     print('SET_PROGRESS add', num, 'to', self.draw_progress, 'of', self, 'direct', direction)
    #     self.draw_progress += num * self.progress_unit
    #     if self.draw_progress <= view_vec(0, 0):
    #         self.draw_progress = 0
    #         if direction == 'up':    return self.up_obj
    #         if direction == 'down':  return self.down_obj
    #         if direction == 'left':  return self.left_obj
    #         if direction == 'right': return self.right_obj
    #         assert False
    #     if self.draw_progress >= unit + LINE_WIDTH:
    #         self.draw_progress = unit + LINE_WIDTH
    #         if direction == 'up':    return self.up_obj
    #         if direction == 'down':  return self.down_obj
    #         if direction == 'left':  return self.left_obj
    #         if direction == 'right': return self.right_obj
    #         assert False
    #     return 1
    # def full_progress(self): 
    #     print(Fore.GREEN+'SET_PROGRESS full from', self.draw_progress, Fore.GREEN+'of', self, Fore.GREEN+'direct', direction)
    #     self.draw_progress = unit + LINE_WIDTH
    # def clear_progress(self): 
    #     print(Fore.GREEN+'SET_PROGRESS clear from', self.draw_progress, Fore.GREEN+'of', self, Fore.GREEN+'direct', direction)
    #     self.draw_progress = 0







'on mouse move'

    # for p in all_point:
    #     if all_point[p].collide(now_mouse_pos): # at turning
    #         print(Fore.MAGENTA+'at', p, MMDA, Fore.MAGENTA+'slope', d.slope)
    #         if -MMDA < d.slope < MMDA: # horizonal
    #             progress = d.x
    #             last_mouse_pos += (d:=view_vec(d.x, 0))
    #             direction = 'horizonal'
    #             if progress > 0: now_line = point(p).right_line
    #             else:            now_line = point(p).left_line
    #             if drawed_line != []:
    #                 if p == drawed_line[-1][0]:
    #                     if drawed_line[-1][1] != now_line:
    #                         drawed_line[-1][1].clear_progress()
    #                         drawed_line.pop()
    #                         print(Back.MAGENTA+Fore.GREEN+'pop horizon')
    #                 else: # has passed
    #                     drawed_line[-1][1].full_progress()
    #             if not (p, now_line) in drawed_line:
    #                 drawed_line.append((p, now_line))
    #                 print(Back.MAGENTA+Fore.GREEN+'append horizon:', drawed_line)
    #         elif d.slope > (1 / MMDA) or d.slope < -(1 / MMDA): # vertical
    #             # TODo negitive slope
    #             progress = d.y
    #             last_mouse_pos += (d:=view_vec(0, d.y))
    #             direction = 'vertical'
    #             # if now_line is None:
    #             if progress > 0: now_line = point(p).down_line
    #             else:            now_line = point(p).up_line
    #             if drawed_line != []:
    #                 if p == drawed_line[-1][0]:
    #                     if drawed_line[-1][1] != now_line:
    #                         drawed_line[-1][1].clear_progress()
    #                         drawed_line.pop()
    #                         print(Back.MAGENTA+Fore.GREEN+'pop vertic')
    #                 else:
    #                     drawed_line[-1][1].full_progress()
    #             if not (p, now_line) in drawed_line:
    #                 drawed_line.append((p, now_line))
    #                 print(Back.MAGENTA+Fore.GREEN+'append vertic:', drawed_line)
    #         else: print('miss', end=''); continue
    #         print(Fore.RED+'prog:', progress, Fore.RED+'d:', d, 
    #               '\n '+Fore.CYAN+'direction', direction, Fore.CYAN+'now_line', now_line, 
    #               '\n '+Fore.YELLOW+'draw_line', drawed_line)
    #         break
    # else: # not at turning
    #     print('=', end='')
    #     if direction == 'horizonal':
    #         progress = d.x
    #         last_mouse_pos += (d:=view_vec(d.x, 0))
    #     elif direction == 'vertical':
    #         progress = d.y
    #         last_mouse_pos += (d:=view_vec(0, d.y))
    #     else: return #error
    # if now_line is None:
    #     if drawed_line != []: drawed_line.pop()
    #     last_mouse_pos -= d
    #     print(Back.MAGENTA+Fore.GREEN+'pop nowlineNone:', drawed_line)
    #     now_line = drawed_line[-1][1] if drawed_line!=[] else None
    #     print('try to enter line not exist at point')
    #     return # try to enter line not exist at point
    
    # res = now_line.set_progress(
    #     ('up' if progress < 0 else 'down')
    #     if direction!='horizonal'
    #     else ('left' if progress < 0 else 'right'), 
    #     progress
    # )
    # if res == 1: pass# work well
    # elif res == -1: # line cannot pass
    #     last_mouse_pos -= d
    # elif res: # line
    #     now_line = res
    # else: # not exist
    #     if now_line.right_is_end(): return 'END'
    #     last_mouse_pos -= d









    # region deleted
# direction: Literal['horizonal', 'vertical']|None = None
# now_line: line = None
# drawed_line: list[tuple[vec2, line]] = [] # turning, line
# _opposite_direction_list: Final = ['left', 'right', 'left', 'up', 'down', 'up']
# def opposite_direction(dir):
#     return _opposite_direction_list[_opposite_direction_list.index(dir)+1]

# def on_mouse_move(now_mouse_pos: view_vec):
#     # pass
#     print(0)
#     global direction, now_line, decision_pos, mouse_reset_pos, dcs_p_pos1, dcs_point
#     d = now_mouse_pos - decision_pos
#     print(Back.GREEN+Fore.YELLOW+'dcs_p:'+repr(decision_pos)+'; nmp:'+repr(now_mouse_pos)+'; d:'+repr(d)+Fore.RESET+Back.RESET)
#     if d == view_vec(0, 0): print(-1); return
#     # check turing
#     for p in [point(now_line.pos1), point(now_line.pos2)] if now_line else [point(point_start)]:
#         if p.collide(now_mouse_pos): # at turning
#             decision_pos = p2vpo(p, (LINE_WIDTH/2, LINE_WIDTH/2))
#             d = now_mouse_pos - decision_pos
#             print(Back.GREEN+Fore.YELLOW+'att, dcs_p:'+repr(decision_pos)+'; nmp:'+repr(now_mouse_pos)+'; d:'+repr(d)+Fore.RESET+Back.RESET)
#             print('slope:', d.slope)
#             if -MMDA < d.slope < MMDA: # horizonal
#                 print(Back.MAGENTA+Fore.YELLOW+'horizonal')
#                 d.y = 0
#                 if  d.x > 0                    and \
#                     not p.right_line is None   and \
#                     not now_line == p.right_line:
#                     now_line   = p.right_line
#                     dcs_p_pos1 = True
#                 elif d.x < 0                   and \
#                      not p.left_line is None   and \
#                      not now_line == p.left_line:
#                     now_line   = p.left_line
#                     dcs_p_pos1 = False
#                 # else: assert False # how come I wrote this?
#             elif -1/MMDA > d.slope or d.slope > 1/MMDA: # vertical
#                 print(Back.MAGENTA+Fore.YELLOW+'vertical')
#                 d.x = 0
#                 if  d.y > 0                    and \
#                     not p.down_line is None    and \
#                     not now_line == p.down_line: 
#                     now_line   = p.down_line
#                     dcs_p_pos1 = True
#                 elif d.y < 0                   and \
#                      not p.up_line is None     and \
#                      not now_line == p.up_line:
#                     now_line   = p.up_line
#                     dcs_p_pos1 = False
#             else:
#                 print(Back.MAGENTA+Fore.YELLOW+'at_turning_but_miss')
#                 return
#             break
#     else:
#         print(Back.MAGENTA+Fore.YELLOW+'not_at_turing')
#         pass
#     if dcs_point.to_end(): # TODo prettier => vec2 compare, needn't fixing!
#         print(Back.GREEN+Fore.YELLOW+'end', now_line, d)
#         return 'END'
#     lnl = now_line
#     now_line, addition = now_line.passed_add(d, dcs_p_pos1)
#     # assert not now_line is None # maybe it is simple
#     if now_line is None:
#         now_line = lnl
#     # decision_pos = now_line.pos1
#     # assert decision_pos == p2vpo(now_line.pos1, (LINE_WIDTH/2, LINE_WIDTH/2)), p2vpo(now_line.pos1, (LINE_WIDTH/2, LINE_WIDTH/2))
#     addition = now_line.process_unit * addition
#     now_line.draw_progress = addition
#     mouse_reset_pos = decision_pos + d
# endregion





















'-------------------------240610-----------------------------'
'past func'

# def _fill(point, horizonalon, positiveon):
#     target = _near_line(point, horizonalon, positiveon)
#     if target and target.draw_progress.length != 0:
#         target.fill()
# _available = lambda point, horizonalon, positiveon: not _near_line(point, horizonalon, positiveon) is None and _near_line(point, horizonalon, positiveon).draw_progress.length == 0 and _near_line(point, horizonalon, positiveon).type != 'line_cannot_pass'
# _available = lambda point, horizonalon, positiveon: not _near_line(point, horizonalon, positiveon) is None and _near_line(point, horizonalon, positiveon).draw_progress.length == 0 and _near_line(point, horizonalon, positiveon) != now_line and _near_line(point, horizonalon, positiveon).type != 'line_cannot_pass'
# _fill = lambda point, horizonalon, positiveon: _near_line(point, horizonalon, positiveon) and _near_line(point, horizonalon, positiveon).draw_progress.length != 0 and _near_line(point, horizonalon, positiveon).fill()
# def _set_nowl(point, horizonalon, positiveon):
#     global now_line
#     now_line = _near_line(point, horizonalon, positiveon)

# _near_line = lambda point, horizonalon, positiveon: (
#     (point.right_line if positiveon else point.left_line)
#     if horizonalon
#     else (point.down_line if positiveon else point.up_line)
# )
# TODo \|/ check ne "now_line" finished | fixed on 240607 or so

# def property_cache(f):
#     @property
#     @lru_cache
#     def res(*args, **kwargs):
#         # if cse.call_process() != 'prs': print(cse.call_process(), args)
#         return f(*args, **kwargs)
#     return res

'unused var'

# last_mouse_pos = view_vec(0, 0)
# decision_pos: view_vec = view_vec(0, 0)
# dcs_p_pos1: bool = True
# dcs_point: point = None
# mouse_reset_pos:view_vec = view_vec(0, 0)
# last_mouse_pos = view_vec(0, 0)

'at turning change'

        # # only left2right | right2left
        # if d.positive: # left2right
        #     if available(turning, True, True):
        #         _danfh = danfh(turning, True, True)
        #         set_state(h, _danfh, t, t)
        #         if not _danfh: fill_an(turning, True, True, unit)
        # else: # right2left
        #     if available(turning, True, False):
        #         _danfh = danfh(turning, True, False)
        #         set_state(h, _danfh, t, f)
        #         if not _danfh: fill_an(turning, True, False, unit)



        
        # assert self.draw_progress.x >= 0 and self.draw_progress.y >= 0
        # draw_line(surface, line_color['draw'], 
        #           p2vpo(self.pos1, self.draw_offset).to_tuple(), 
        #           p2vpo(self.pos1, tuple_sum(self.draw_progress, self.draw_offset)).to_tuple(),
        #           LINE_WIDTH, self.horizonal)

        # think twice before changing this
        # if self.draw_progress.positive:
        #     draw_line(surface, line_color['draw'], 
        #             p2vpo(self.pos1, self.draw_offset).to_tuple(), 
        #             p2vpo(self.pos1, self.draw_progress).to_tuple(),
        #             LINE_WIDTH, self.horizonal)
        # else:
        #     draw_line(surface, line_color['draw'], 
        #             p2vpo(self.pos1, self.draw_offset).to_tuple(), 
        #             p2vpo(self.pos1, self.area-self.draw_progress).to_tuple(),
        #             LINE_WIDTH, self.horizonal)
        # TODO complete

'class line'

    # deleted
    # def to(self, forward_on):
    #     return (self.right_obj if forward_on else self.left_obj) if self.horizonal \
    #            else (self.down_obj if forward_on else self.up_obj)
    # def passed_add(self, d, dcs_p_pos1: bool) -> tuple[Self, int]: # change d, chack turing before calling
    #     # d: about dcs p
    #     # d_int = 0
    #     if self.horizonal: d.y = 0; d_int = d.x
    #     else: d.x = 0; d_int = d.y
    #     # if else complete
    #     if dcs_p_pos1:
    #         if d_int > 0 and d_int > self.area.length:
    #             # change rest part: self.area-self.draw_progress
    #             d_int -= self.area.length
    #             self.fill()
    #             return (self.right_obj if self.horizonal else self.down_obj), d_int
    #         if d_int < 0 and -d_int > self.draw_progress.length:
    #             # change drawed part: self.draw_progress
    #             d_int += self.draw_progress.length
    #             self.clear()
    #             return (self.left_obj if self.horizonal else self.up_obj), d_int
    #     else:
    #         if d_int > 0 and d_int > self.draw_progress.length:
    #             # change drawed part: self.draw_progress
    #             d_int -= self.draw_progress.length
    #             self.clear()
    #             return (self.right_obj if self.horizonal else self.down_obj), d_int
    #         if d_int < 0 and -d_int > (self.area-self.draw_progress).length:
    #             # change rest part: self.area-self.draw_progress
    #             d_int += (self.area-self.draw_progress).length
    #             self.fill()
    #             return (self.left_obj if self.horizonal else self.up_obj), d_int
    #     return self, d_int
    # def full_progress(self): 
    #     self.draw_progress = self.area

    
    # @property
    # @lru_cache
    # def to_end(self, d): return self.horizonal and d.x > 0 and self.pos2 == point_end
    # @property
    # def process_unit(self):
    #     return view_vec(1, 0) if self.horizonal else view_vec(0, 1)
    