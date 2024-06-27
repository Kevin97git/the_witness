from random import randint, Random
from copy import copy
# from functools import cmp_to_key, lru_cache
# from itertools import groupby
# from sys import _getframe
from colorama import Fore, init
init(True)
import multiprocessing as mp
from multiprocessing import Pipe
from multiprocessing.connection import PipeConnection
import asyncio
import pprint
from typing import Literal
import numpy as np

from paint_classes import (point, line, square, pos2, 
                           set_a, event_loop, main_draw, set_by_puzzle, get_surface, set_caption,
                           set_visible, set_grab, get_grab,
                           main_clock)
from config_save_error import raise_error, log, get_key_val, set_key_val
from constant_type import *



# region type
once = Any
shape = Any
puzzle_square_type = dict[pos2, list[cse.basic.poss_cls_sq]]
line_id = str
puzzle_line_type = dict[line_id, cse.basic.poss_cls_l]
puzzle_type = tuple[puzzle_square_type, puzzle_line_type]
# endregion
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
        # n.sort(key=cmp_to_key(list_compare))
        parts.append(n)
    return parts
def get_parts_for_check(squares: list[square]):
    parts: list[list[square]] = []
    while len(squares) != 0:
        s: square = squares[0]
        n = s.near_samep_for_check()
        n.append(s)
        done = [s]
        while len(n) != len(done):
            i = 0
            for i in range(len(n)):
                if not n[i] in done: break
            done.append(n[i])
            n += n[i].near_samep_for_check(); n = list(set(n))
            i = 0
        for e in n:
            squares.remove(e)
        parts.append(n)
    return parts
def print_parts(parts, a):
    for y in range(a):
        string = ''
        for x in range(a):
            for ind, sl in enumerate(parts):
                if square(pos2(x, y)) in sl:
                    string += str(ind)
        print(' '.join(string))
def choice_sq_possibilities(rand, possibilities: puzzle_square_type, a:int) -> puzzle_square_type:
    # TODO upside down Y
    keys = list(possibilities.keys()) # get each square
    res: puzzle_square_type = {}
    rand.shuffle(keys)
    # keys = keys[int(a * a * PSP):]
    keys = keys[:rand.randint(int(a * a * PSPI), int(a * a * PSPA))]
    for k in keys:
        # V: once(obj: tuple[shape, pos2])
        tmp = rand.choice([ e for e in possibilities[k] if e.available ])
        res[k] = tmp.collapse(rand)
    return res
def choice_l_possibilities(rand, possibilities:dict, a:int) -> puzzle_line_type:
    res = {}
    for k in copy(possibilities):
        if possibilities[k] == []:
            possibilities.pop(k)
    keys = list(possibilities.keys()) # get each line
    rand.shuffle(keys)
    keys = keys[:rand.randint(
        min(int(a * a * PLPI), len(keys)),
        min(int(a * a * PLPA), len(keys))
    )]
    for k in keys:
        tmp = rand.choice([ e for e in possibilities[k] if e.available ])
        res[k] = tmp.collapse(rand)
    return res
        
puzzle_size_path_init = puzzle_module_load_func('puzzle_size_path_init')
square_poss_cls:list[cse.basic.poss_cls_sq] = []
for cls_name in cse.basic.square_poss:
    square_poss_cls.append(puzzle_module_load_cls(cls_name))
line_poss_cls:list[cse.basic.poss_cls_l] = []
for cls_name in cse.basic.line_poss:
    line_poss_cls.append(puzzle_module_load_cls(cls_name))
def _reset(seed1: int, seed2: int) -> tuple[puzzle_type, int, pos2, pos2]:
    square_possibilities:puzzle_square_type = {}
    # seed(SMM(seed1, seed2)) # TODO mod loader
    rand = Random(SMM(seed1, seed2)) # TODO mod loader
    log(f'reset: seed1={seed1}, seed2={seed2}, mix={SMM(seed1, seed2)}')
    a = puzzle_size_path_init(rand)

    # possibilities init here, each of them are list
    cpy_asv = copy(list(square.all().values()))
    for s in cpy_asv: square_possibilities[s.pos] = []
    
    # get parts
    # cpy_asv = copy(list(square.all().values()))
    parts = get_parts(squares=cpy_asv)
    print(Fore.BLUE + 'parts_num: ' + str(len(parts)))

    for poss_cls in square_poss_cls:
        poss_cls.update_poss(rand, cpy_asv, parts, square_possibilities)

    log('poss: '+repr(square_possibilities))
    puzzle_square = choice_sq_possibilities(rand, square_possibilities, a=a)
    print(puzzle_square)
    # puzzle_lines = rand.sample(copy(line.all().values()), puzzle_line_num)
    cpy_alv = copy(list(line.all().values()))
    line_possibilities = {}
    for l in cpy_alv:
        line_possibilities[l.id] = []
    for poss_cls in line_poss_cls:
        poss_cls.update_poss(rand, cpy_alv, line_possibilities)
    puzzle_line = choice_l_possibilities(rand, line_possibilities, a)
    # splited_lines = split_sequence(rand, puzzle_lines, 2)
    # line_cls = [LMP, LCP]
    # for el, _cls in zip(splited_lines, line_cls):
    #     for k in el:
    #         puzzle_line[k.id] = _cls()
    puzzle: puzzle_type = (puzzle_square, puzzle_line)
    # TODO CHECK
    square.clear()
    line.clear_alll()
    point.clear()
    log('reset end. prs clear end.')
    return puzzle, a, cse.basic.cache.point_start.pos, cse.basic.cache.point_end.pos
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
def check_answer(puzzle: puzzle_type, a) -> bool:
    cse.basic.cache.a = a
    puzzle_square, puzzle_line = puzzle
    for lid in puzzle_line:
        l = line.by_id(lid)
        cse.log(f'checking {lid}, content={l.type}')
        if not l.type.check(l):
            cse.log(f'check_answer return false')
            return False
    parts = get_parts_for_check(copy(list(square.all().values())))
    for sdp in puzzle_square:
        sq = square(sdp)
        cse.log(f'checking {sdp}, content={sq.content}')
        if not sq.content.check(parts, sq):
            cse.log(f'check_answer return false')
            return False
    cse.log(f'check_answer return true')
    return True

def game_loop(puzzle: puzzle_type, a: int, p_start:pos2, p_end:pos2, surface):
    set_a(a)
    square.clear()
    line.clear_alll()
    point.clear()
    # print(puzzle, a, p_start, p_end)
    square.set_by_a(a)
    print(puzzle[0])
    set_by_puzzle(puzzle, p_start, p_end)
    main_draw(surface)
    while True: # TODO
        cmd = event_loop()
        match cmd:
            case 'END_CHECK':
                correcton = check_answer(puzzle, a)
                if correcton:
                    return 'NEXT'
                line.clear_all_progress()
            case 'EXIT'|'NEXT'|'RESTART': return cmd
            case 'MOUSE_UNLOCK':
                if get_grab():
                    set_visible(True)
                    set_grab(False)
                    log('set visible=True, grab=False')
                else:
                    set_visible(False)
                    set_grab(True)
                    log('set visible=False, grab=True')
            case 'DRAW_UPDATE': main_draw(surface)
            case None: pass
            case _: assert False
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
    def new_puzzle_by(seed1, seed2, prs: mp.Process, surface): # __main__
        print('in new_puzzle_by')
        set_visible(False)
        set_grab(True)
        log('set visible=False, grab=True')
        prs_puzzle_pipe_main.send((seed1, seed2))
        print('main: send end')
        while True: # TODO
            res: tuple[puzzle_type, int, pos2, pos2]|None = prs_puzzle_pipe_main.recv()
            if res: 
                seed2 += 1
                prs_puzzle_pipe_main.send((seed1, seed2))
                cmd = game_loop(res[0], res[1], res[2], res[3], surface)
                if cmd == 'EXIT':
                    prs.terminate()
                    prs_puzzle_pipe_main.close()
                    prs_puzzle_pipe_sub.close()
                    set_visible(True)
                    set_grab(False)
                    return
                if cmd == 'NEXT': continue
                if cmd == 'RESTART': return 'RESTART'
            else:
                seed2 += 1
                print('timeout')
                prs_puzzle_pipe_main.send((seed1, seed2))
                # prs.join(PGT+1)
            set_key_val('seed2', seed2)
    seed1 = get_key_val('seed1')
    if seed1 == -1:
        seed1 = randint()
        set_key_val('seed1', seed1)
    seed2 = get_key_val('seed2')
    res = True
    while res:
        res = new_puzzle_by(seed1=seed1, seed2=seed2, prs=prs, surface=main_surface)
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
    check in main,
    y:  goto puzzle_generate_loop
    n:  goto game_loop

'''