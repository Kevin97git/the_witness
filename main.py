from random import choice, choices, randint, shuffle, seed
from copy import copy
from functools import cmp_to_key
from itertools import groupby
from sys import _getframe
from colorama import Fore, init
init(True)
import multiprocessing as mp
from multiprocessing import Pipe
from multiprocessing.connection import PipeConnection
import asyncio
import pprint
from typing import Literal

from paint_classes import (point, line, square, vec2, 
                           grid, shape, once, 
                           set_a, event_loop, main_draw, set_by_puzzle, get_surface, set_caption, 
                           set_visible, set_grab, get_grab,
                           main_clock, 
                           shape_length_minimum)
from config_save_error import raise_error, log, get_key_val, set_key_val
from constant_type import *


# Return random integer in range [a, b).
def _rand(a: int, b: int): return randint(a, b-1)
def _rand_bool(a:int, b:int): return 0 in choices([i for i in range(b)], k=a)

#debug
# def debug_print_all_line():
#     for k in line.all():
#         if line.all()[k].exist:
#             print(k)
# def debug_flag(): print('flag')



def path_sidesway(l: line):
    while True:
        if l.horizonal: return False
        if not l.exist: return False
        #left
        if (
            (not l.left_obj is None)
            and (not l.left_obj.exist)
            and (not line(l.p1.left_obj, l.p1).exist)
            and (not l.p1.left_obj.passed)
            and (not line(l.p2.left_obj, l.p2).exist)
            and (not l.p2.left_obj.passed)
        ):
            if _rand_bool(1, 4):
                l.left_obj.on()
                l.off()
                line(l.p1.left_obj, l.p1).on()
                line(l.p2.left_obj, l.p2).on()
                continue
            else: break
        if (
            (not l.right_obj is None)
            and (not l.right_obj.exist)
            and (not line(l.p1, l.p1.right_obj).exist)
            and (not l.p1.right_obj.passed)
            and (not line(l.p2, l.p2.right_obj).exist)
            and (not l.p2.right_obj.passed)
        ):
            if _rand_bool(1, 4):
                l.right_obj.on()
                l.off()
                line(l.p1, l.p1.right_obj).on()
                line(l.p2, l.p2.right_obj).on()
                continue
            else: break
        return False
def list_compare(x:square, y:square):
    if x.pos.y > y.pos.y: return 1
    elif x.pos.y < y.pos.y: return -1
    else:
        if x.pos.x > y.pos.x: return 1
        else: return -1
# def destribute(l1:list, l2:list):
#     return [l1+[e] for e in l2]


match_item_type = tuple[shape, vec2, grid]
match_end_type  = list [match_item_type]
shape_prob_type = tuple[shape, vec2]
# (match end: have the same shape, prob, len(match_end))
state_item_type = tuple[list[match_item_type], list[shape_prob_type], int]
prob_type = dict[vec2, 
                 list[
                 tuple[Literal['line_passed_number: '], int]
                 | tuple[Literal['part_index: '], int]
                 | tuple[Literal['shape_unrotatable: '], once]
                 | tuple[Literal['shape_rotatabele: '], once]]
                ]
puzzle_square_type = dict[vec2, 
                          tuple[Literal['line_passed_number: '], int]
                          | tuple[Literal['part_index: '], int]
                          | tuple[Literal['shape_rotatable: '], shape]
                          | tuple[Literal['shape_unrotatable: '], shape]
                         ]
line_id = str
puzzle_line_type = dict[line_id, 
                        Literal['line_must_pass']
                        |Literal['line_cannot_pass']
                        ]
puzzle_type = tuple[puzzle_square_type, puzzle_line_type]

def _remove(l:list, item) -> list:
    l.remove(item)
    return l
# get a state-like object to be added into state
def _match(g:grid, 
           prob:list[shape_prob_type], 
           prefix:list = [],
           length:int  = 0
    )->list[state_item_type]: 
    # print('_match g:', g, 'prob:', prob if len(prob) < 8 else len(prob), 'len_prefix:', len(prefix), 'length:', length)
    res: list[state_item_type] = []
    # foreach probabilities in order to match by
    for s in prob:
        me, rprob = g.match_prefix(s, prefix=prefix)
        # rprob: all probabilities for matching g
        if me == []: continue
        res += [(mee, _remove(rprob, s), length) for mee in me if rprob != [s]] # delete matched
    shuffle(res)
    return res
def match(g:grid) -> list[match_item_type]:
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
    for s in shape.all():
        # me: only one shape
        me, sprob = g.match(s)
        prob += sprob
        mel += me
    if mel == []: return []
    # length equals to 1
    maximum = choice(mel)
    # if type(maximum) != list or (maximum != [] and type(maximum[0]) != tuple):
    #     assert False
    maximum_len = 1
    for e in mel:
        tmp = copy(prob); tmp.remove((e[-1][0], e[-1][1]))
        if tmp == []: continue
        state.append((e, tmp, 1))
    if state == []: return []
    # print('prob init.\nloop begins')
    
    while True:
        state_now = state[-1]
        state.pop()
        prob = state_now[1]       # what the grid may include
        assert prob != []
            # print('prob == [], state:', state if len(state) < 8 else len(state))
            # state.pop() #err
            # continue
        now = state_now[0][0][2] # what to match
        res = _match(now, prob, prefix=state_now[0], length=state_now[2]+1)
        # if type(res) != list or (res != [] and (type(res[0]) != tuple or type(res[0][0]) != list or type(res[0][1]) != list or type(res[0][2]) != int)):
        #     assert False
        if res == []: # match nothing
            # print('match nothing')
            # state.pop()
            if state == []:
                if type(maximum) != list or (maximum != [] and type(maximum[0]) != tuple):
                    assert False
                # print('match return max:', maximum)
                return maximum
            continue
        else:
            # print('-----match sth-----')
            if res[-1][2] >= shape_length_minimum:
                # print('match return:', res)
                # if type(res[-1][0]) != list or (res[-1][0] != [] and type(res[-1][0][0]) != tuple):
                #     assert False
                return res[-1][0]
            if res[-1][2] > maximum_len:
                maximum_len = res[-1][2]
                # if type(res[-1][0]) != list or (res[-1][0] != [] and type(res[-1][0][0]) != tuple):
                #     assert False
                maximum = res[-1][0]
            state += res
def get_parts(squares: list[square]):
    # print('begin squares', squares)
    parts: list[list[square]] = []
    while len(squares) != 0:
        s: square = squares[0]
        n = s.near_samep()
        n.append(s)
        done = [s]
        while len(n) != len(done):
            i = 0
            for i in range(len(n)):
                if not n[i] in done: break
            done.append(n[i])
            n += n[i].near_samep(); n = list(set(n))
            i = 0
        
        for e in n:
            # if not e in squares: print(e); print(squares)
            squares.remove(e)
        n.sort(key=cmp_to_key(list_compare))
        parts.append(n)
    return parts
def print_parts(parts, a):
    for y in range(a):
        string = ''
        for x in range(a):
            for ind, sl in enumerate(parts):
                if square(vec2(x, y)) in sl:
                    string += str(ind)
        print(' '.join(string))
def choice_probabilities(probabilities: prob_type, a:int) -> puzzle_square_type:
    # TODO upside down Y
    keys = list(probabilities.keys())
    res: puzzle_square_type = {}
    shuffle(keys)
    keys = keys[int(a * a * PSP):]
    # log('keys: '+repr(keys))
    for k in keys:
        # log('choicing key: '+repr(k))
        # V: once(obj: tuple[shape, vec2])
        tmp = choice([e for e in probabilities[k] if (not e[0] in (SU, SR)) or (e[1].available)])
        T, V = tmp
        if T == SU:
            V.use()# v.obj: tuple[shape, vec2]
            res[k] = (T, V.obj[0])
        elif T == SR:
            V.use()
            res[k] = (T, shape(V.obj[0].pattern, randint(0, 3)))
        else:
            res[k] = (T, V)
    return res
def _reset(seed1: int, seed2: int) -> tuple[puzzle_type, int, vec2, vec2]:
    probabilities:prob_type = {}
    seed(SMM(seed1, seed2))
    log(f'reset: seed1={seed1}, seed2={seed2}, mix={seed1^seed2}')
    a = randint(A_MIN, A_MAX)
    set_a(a)
    square.set_by_a(a)
    # rand important point
    point_start   = point(vec2(0, randint(0, a)))
    point_end     = point(vec2(a, randint(0, a)))
    turning_point = [ point(vec2(i, randint(0, a))).on() for i in range(a) ]
    if point_start is None or point_end is None or None in turning_point:
        raise_error('Any of important point is none')
    point_start.on()
    point_end.on()

    # connect them
    last = point_start
    for p in turning_point:
        if p != last: line.from_to_untidy(p, last)
        last = p.right_obj
        line(p, last).on()
    if last != point_end: line.from_to_untidy(last, point_end)
    # sidesway
    for l in copy(list(line.all().values())): path_sidesway(l)
    # probabilities init here, each of them are list
    # add probabilities: LPN
    cpy_asv = copy(list(square.all().values()))
    for s in cpy_asv:
        t = s.line_passed
        probabilities[s.pos] = [] if t == 0 else [(LPN, t)]
    # get parts
    cpy_asv = copy(list(square.all().values()))
    parts = get_parts(squares=cpy_asv)
    print(Fore.BLUE + 'parts_num: ' + str(len(parts)))
    # add probabilities: PI
    for ind, p in enumerate(parts):
        for e in p:
            if ind < len(PI_color): # TODO just for color but need shuffling
                probabilities[e.pos].append((PI, ind))
        g = grid(p)
        sub_pro: list[match_item_type] = match(g)

        if sub_pro != []:
            print(sub_pro)
            tmp = []
            for i in sub_pro:
                _once = once(i[:2])
                tmp.append((SU, _once))
                tmp.append((SR, _once))
                
            for squ in p: probabilities[squ.pos] += tmp

    log('prob: '+repr(probabilities))
    puzzle_square = choice_probabilities(probabilities=probabilities, a=a)
    print(puzzle_square)
    puzzle_line_num = randint(int(PLPI*(2*a*a+2*a)), int(PLPA*(2*a*a+2*a)))
    on_num = randint(0, puzzle_line_num)
    off_num = puzzle_line_num - on_num
    on, off = line.classify()
    # print('------------', on, off)
    on = choices(on, k=min(on_num, len(on)))
    off = choices(off, k=min(off_num, len(off)))
    # print('============', on, off)
    puzzle_line = {}
    for k in on: puzzle_line[k.id] = LMP
    for k in off: puzzle_line[k.id] = LCP
    puzzle: puzzle_type = (puzzle_square, puzzle_line)
    # TODO CHECK
    square.clear()
    line.clear()
    point.clear()
    log('reset end. prs clear end.')
    return puzzle, a, point_start.pos, point_end.pos
def call_reset(puzzle_pipe:PipeConnection, timeout=None):
    print('call_reset loop_begin')
    async def reset():
        try:
            async with asyncio.timeout(timeout):
                res = _reset(seed1, seed2)
        except asyncio.TimeoutError as e:
            print('async.timeout Timeout:', timeout, e)
            res = None
        return res
    while True:
        message = puzzle_pipe.recv()
        print('call reset:recv end')
        if type(message) == tuple:
            seed1, seed2 = message
            print('call reset:reset begin')
            res = asyncio.run(reset())
            # print('call reset:reset end', res)
            print('call reset:reset end')
            puzzle_pipe.send(res)
            # recieve at 412 then to 382
            print('call reset:send end')
        # elif type(message) == str:
        #     match message:
        #         case 'EXIT':
        #             pipe.send('Function Return')
        #             return
def game_loop(puzzle: puzzle_type, a: int, p_start:vec2, p_end:vec2, surface):
    set_a(a)
    square.clear()
    line.clear()
    point.clear()
    # print(puzzle, a, p_start, p_end)
    square.set_by_a(a)
    print(puzzle[0])
    set_by_puzzle(puzzle, p_start, p_end)
    main_draw(surface)
    while True: # TODO
        cmd = event_loop()
        if cmd in ('EXIT', 'NEXT', 'END'):
            return cmd
        if cmd == 'MOUSE_UNLOCK':
            if get_grab():
                set_visible(True)
                set_grab(False)
                log('set visible=True, grab=False')
            else:
                set_visible(False)
                set_grab(True)
                log('set visible=False, grab=True')
        if cmd == 'DRAW_UPDATE':
            main_draw(surface)
        # main_draw(surface)
        main_clock.tick(TICK)

if __name__ == '__main__':
    print('__main__')
    log('start')
    prs_puzzle_pipe_main, prs_puzzle_pipe_sub = Pipe()
    # prs_list_pipe_main, prs_list_pipe_sub = Pipe()
    prs = mp.Process(target=call_reset, args=(prs_puzzle_pipe_sub, PGT), name='prs')
    prs.start()
    main_surface = get_surface()
    set_caption('the_witness')
    def new_puzzle_by(seed1, seed2, prs: mp.Process, pca: mp.Process, surface): # __main__
        print('in new_puzzle_by')
        set_visible(False)
        set_grab(True)
        log('set visible=False, grab=True')
        prs_puzzle_pipe_main.send((seed1, seed2))
        print('main: send end')
        while True: # TODO
            res: tuple[puzzle_type, int, vec2, vec2]|None = prs_puzzle_pipe_main.recv()
            if res: 
                seed2 += 1
                prs_puzzle_pipe_main.send((seed1, seed2))
                cmd = game_loop(res[0], res[1], res[2], res[3], surface)
                if cmd == 'EXIT':
                    prs.terminate()
                    # pca.terminate()
                    prs_puzzle_pipe_main.close()
                    prs_puzzle_pipe_sub.close()
                    set_visible(True)
                    set_grab(False)
                    return
                if cmd == 'NEXT': continue
                if cmd == 'END':
                    pass
            else:
                seed2 += 1
                print('timeout')
                prs_puzzle_pipe_main.send((seed1, seed2))
                # prs.join(PGT+1)
            set_key_val('seed2', seed2)
    cmdl = []
    with open('./TODO', 'r') as f:
        while (cmd := f.readlines()) != '' and len(cmdl) < CMDRM:
            cmdl.append(cmd)
    for cmd in cmdl: # TODO
        if cmd == []: continue
        args = cmd[1:]
        cmd = cmd[0]
        argnum = len(cmd[1:])
        match cmd[0]:
            case 'RESET':
                if argnum != 2: raise_error(f'run RESET command, expect 2 args but {argnum} were given')
                new_puzzle_by(seed1=argnum[0], seed2=argnum[1])
            case _:
                pass
    print('cmd run end')
    seed1 = get_key_val('seed1')
    if seed1 == -1:
        seed1 = randint()
        set_key_val('seed1', seed1)
    seed2 = get_key_val('seed2')
    new_puzzle_by(seed1=seed1, seed2=seed2, prs=prs, pca=None, surface=main_surface)
    # seed2 += 1
    # set_key_val('seed2', seed2)
'''
start.
check command.
call_reset: 
    reset in prs, 

    flag puzzle_generate_loop
    pipe to main, 
    draw in main, 
    reset in prs, 

    flag game_loop
    wait finish,
    check in pca,
    y:  goto puzzle_generate_loop
    n:  goto game_loop

'''
# reset(1, 1919810)
# loop()