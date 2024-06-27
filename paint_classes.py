import pygame
pygame.init()
import pygame.draw as draw
import pygame.gfxdraw as gfxdraw
import pygame.locals
from pygame.display import set_caption
from collections import namedtuple
from functools import lru_cache
from typing import List, Any, Self, Literal, Callable, Final
from copy import copy
from numpy import ndarray
import numpy as np
import math
import sys
from colorama import Fore, init, Back
init(True)

import config_save_error as cse
from constant_type import *
import about_mouse as am

class pos2(namedtuple('pos2_super', 'x y')):
    __slots__ = ()
    def __repr__(self):
        return f'v({self.x}, {self.y})'
class view_pos:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    def __sub__(self, other): return view_pos(self.x - other.x, self.y - other.y)
    def __add__(self, other): return view_pos(self.x + other.x, self.y + other.y)
    def __mul__(self, other): return view_pos(self.x * other, self.y * other)
    def __rmul__(self, other): return view_pos(self.x * other, self.y * other)
    def __neg__(self): return view_pos(-self.x, -self.y)
    def __matmul__(self, oth): return self.x * oth + self.y * oth
    def __getitem__(self, key): return [self.x, self.y][key]
    def __repr__(self): return f'vv({self.x}, {self.y})'
    def __eq__(self, oth):
        try:
            return self.x == oth.x and self.y == oth.y
        except:
            return False
    def __lt__(self, oth):
        try: return self.length < oth.length
        except: return False
    def __gt__(self, oth):
        try: return self.length > oth.length
        except: return False
    def __ge__(self, oth): return self == oth or self > oth
    def __hash__(self): return hash((self.x, self.y))
    def to_tuple(self): return (self.x, self.y)
    @property
    def slope(self): return self.y / self.x if self.x != 0 else math.inf
    @property
    def length(self): return math.hypot(self.x, self.y)
    @property
    def positive(self): return self.x >= 0 and self.y >= 0
am.set_view_pos(view_pos)
'''
O ---- x
|
|
y
'''
content_0_0:view_pos = view_pos(x=lr_border, y=tb_border)
def get_surface():
    surf = pygame.display.set_mode(size=(wwidth, wheight), flags=0)
    pygame.key.stop_text_input()
    return surf
main_clock = pygame.time.Clock()
unit = -1
a:int = -1
def set_a(_a: int):
    global a, unit
    a = _a
    unit = int(((wheight - tb_border*2) - (a + 1) * LINE_WIDTH) / a)

def tuple_sum(a:tuple[int|float, int|float], b:tuple[int|float, int|float]): return (a[0] + b[0], a[1] + b[1])
def pos_to_view_pos(pos:pos2):
    return view_pos(
        x=content_0_0.x+pos.x*unit+pos.x*LINE_WIDTH+LINE_WIDTH,
        y=content_0_0.y+pos.y*unit+pos.y*LINE_WIDTH+LINE_WIDTH
    )
def pos_to_view_pos_offset(pos:pos2, offset: tuple[int, int]=(0, 0)): # for line.draw etc.
    return view_pos(
        x=content_0_0.x+pos.x*unit+pos.x*LINE_WIDTH + int(offset[0]),
        y=content_0_0.y+pos.y*unit+pos.y*LINE_WIDTH + int(offset[1])
    )
p2vp = pos_to_view_pos
p2vpo = pos_to_view_pos_offset
am.set_p2vpo(p2vpo)

# region type hints
shape = Any
square_content = Any
# square_content = tuple[Literal['line_passed_number: '], int] \
#                  | tuple[Literal['part_index: '], int] \
#                  | tuple[Literal['shape_rotatable: '], shape] \
#                  | tuple[Literal['shape_unrotatable: '], shape]
content_type = Any
# content_type = Literal['line_passed_number: ', 'part_index: ', 'shape_rotatable: ', 'shape_unrotatable: ']
line_type = Any
# line_type = Literal['line_must_pass'] | Literal['line_cannot_pass'] | Literal['simple']
# endregion



def draw_line(surface, color, start_pos, end_pos, width, horizon) -> pygame.rect.Rect:
    return draw.rect(surface, color, 
                     (start_pos[0], start_pos[1], end_pos[0] - start_pos[0] + width, width)
                     if horizon else (start_pos[0], start_pos[1], width, end_pos[1] - start_pos[1] + width))

all_point:dict[pos2, 'point'] = {}
class point:
    def __new__(cls, pos: pos2):
        if pos in all_point:
            return all_point[pos]
        if pos.x > a or pos.y > a:
            return None
        if pos.x < 0 or pos.y < 0:
            return None
        return super().__new__(cls)
    def __init__(self, pos: pos2):
        if pos in all_point:
            return
        self.x, self.y = pos
        self.pos = pos
        self.passed = False
        all_point[pos] = self
    def on(self): self.passed = True; return self
    def off(self): self.passed = False; return self
    def __repr__(self): return f'({self.pos.x}, {self.pos.y})'
    def __getnewargs__(self): return self.pos
    def __hash__(self): return hash(self.pos)
    @classmethod
    def all(cls): return all_point
    @classmethod
    def clear(cls): global all_point; all_point = {}
    @classmethod
    def set(cls, l): global all_point; all_point = l
    def to_end(self): return self.pos == point_end
    def collide(self, pos: view_pos):
        d = p2vp(self.pos) - pos
        return math.hypot(d.x, d.y) < MCR * unit
    # region near obj
    @property
    def left_obj(self):  return point(pos2(self.x - 1, self.y))
    @property
    def right_obj(self): return point(pos2(self.x + 1, self.y))
    @property
    def up_obj(self):    return point(pos2(self.x, self.y - 1))
    @property
    def down_obj(self):  return point(pos2(self.x, self.y + 1))
    # endregion
    # region near line
    def near_line(self): return [
        self.up_line, self.down_line, 
        self.left_line, self.right_line
    ]
    @property
    def up_line(self): return line(self.up_obj, self)
    @property
    def down_line(self): return line(self, self.down_obj)
    @property
    def left_line(self): return line(self.left_obj, self)
    @property
    def right_line(self): return line(self, self.right_obj)
    def near_line_is_simple(self): return [l for l in self.near_line() if l and l.type.is_simple]
    # endregion
    def draw(self, surface):
        if self.passed:
            print(Fore.GREEN+f'point|{self}:passed'+Fore.RESET)
            viewp = p2vpo(self.pos)
            # draw.rect(surface, (0, 0, 0), (viewp.x, viewp.y, LINE_WIDTH, LINE_WIDTH))
            draw.rect(surface, line_color['draw'], (viewp.x, viewp.y, LINE_WIDTH, LINE_WIDTH))
class _simple:
    def __init__(self):
        self.color = line_color['simple']
        self.passable = True
    @property
    def is_simple(self):
        return True
simple = _simple()
all_line:dict[str, 'line'] = {}
class line:
    def __new__(cls, p1: point, p2: point):
        if p1 is None or p2 is None: return None
        _id = f'{p1};{p2}'
        if _id in all_line: return all_line[_id]
        if p1.x != p2.x and p1.y != p2.y:
            cse.raise_error('class line, __init__, unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
        if p1 == p2:
            cse.raise_error('class line, __init__, unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
        if not p1.x <= p2.x: print(p1.x, p2.x)
        assert p1.x <= p2.x
        return super().__new__(cls)
    def __init__(self, p1: point, p2: point):
        # p1 left or up
        self.id = f'{p1};{p2}'
        if self.id in all_line: return
        self.p1 = p1; self.pos1 = p1.pos
        self.p2 = p2; self.pos2 = p2.pos
        self.type: line_type = simple
        self.draw_progress: am.draw_progress = am.draw_progress.null()
        self.exist = False
        self.horizonal:bool = (p1.y == p2.y)
        all_line[self.id] = self
    # region magic
    def __hash__(self): return hash(self.id)
    def __eq__(self, oth): return isinstance(oth, line) and self.id == oth.id
    # def __repr__(self): return self.id+('T' if self.exist else 'F')+('t' if self.is_on() else 'f')
    def __repr__(self): return self.id+('T' if self.exist else 'F')
    def __getnewargs__(self): return (self.p1, self.p2)
    # endregion
    # region classmethod
    @classmethod
    def all(cls): return all_line
    @classmethod
    def clear_alll(cls): global all_line; all_line = {}
    @classmethod
    def set(cls, l): global all_line; all_line = l
    # @classmethod
    # def classify(cls):
    #     on: list[Self] = []
    #     off: list[Self] = []
    #     for k in all_line:
    #         if all_line[k].exist: on.append(all_line[k])
    #         else: off.append(all_line[k])
    #     return on, off
    @classmethod
    def from_to(cls, p1: point, p2: point):
        if p1.x == p2.x:
            for i in range(0, p2.y - p1.y):
                line(point(pos2(p1.x, p1.y+i)), point(pos2(p1.x, p1.y+i+1))).on()
        elif p1.y == p2.y:
            for i in range(0, p2.x - p1.x):
                line(point(pos2(p1.x+i, p1.y)), point(pos2(p1.x+i+1, p1.y))).on()
        else:
            cse.raise_error('class line, classmethod "from_to", unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
    # endregion
    # region construct method
    @classmethod
    def by_id(cls, _id): return all_line[_id]
    @classmethod
    def from_to_untidy(cls, p1: point, p2: point):
        if p1.x < p2.x or p1.y < p2.y: return cls.from_to(p1, p2)
        if p1.x > p2.x or p1.y > p2.y: return cls.from_to(p2, p1)
        assert False
    @classmethod
    def untidy(cls, p1: point, p2: point):
        if p1.x < p2.x or p1.y < p2.y: return cls(p1, p2)
        if p1.x > p2.x or p1.y > p2.y: return cls(p2, p1)
        assert False
    # endregion
    # region about draw and related variable
    @property
    def draw_offset(self):
        if self.type.is_simple: return (0, 0)
        if point(self.pos1).near_line_is_simple() == []:
            return (0, 0)
        return (LINE_WIDTH, 0) if self.horizonal else (0, LINE_WIDTH)
    def draw(self, surface):
        draw_line(surface, self.type.color, 
                  p2vpo(self.pos1, self.draw_offset).to_tuple(), 
                  p2vpo(self.pos2).to_tuple(),
                  LINE_WIDTH, self.horizonal)
        self.draw_draw_progress(surface)
        self.p1.draw(surface)
        self.p2.draw(surface)
    def on(self):
        self.exist = True
        self.p1.on(); self.p2.on()
        return self
    def off(self):
        self.exist = False
        self.p1.off(); self.p2.off()
        return self
    def set_type(self, type): self.type = type
    def is_on(self): # for check
        return self.draw_progress.progress.length != 0
    
    def draw_draw_progress(self, surface):
        if self.draw_progress.progress == view_pos(0, 0): return
        self.draw_progress.dcsp.on()
        if self.draw_progress.progress == self.area: self.fill()
        assert self.draw_progress.progress.x == 0 or self.draw_progress.progress.y == 0
        # self.draw_progress = self.area if self.draw_progress.length > self.area.length else self.draw_progress
        # print(Fore.BLUE+repr(self)+' '+repr(self.draw_progress)+Fore.RESET)
        p1, p2 = self.draw_progress.to_linese(p2vpo(self.pos1, self.draw_offset), self.area)
        draw_line(surface, line_color['draw'], 
                p1.to_tuple(), 
                p2.to_tuple(),
                LINE_WIDTH, self.horizonal)
        # self.draw_progress.dcsp.draw(surface)
    @classmethod
    def clear_all_progress(cls):
        for l in all_line:
            all_line[l].draw_progress = am.draw_progress.null()
            all_line[l].off()

    @property
    def is_simple_or_has_to_be(self): return self.type.is_simple or point(self.pos1).near_line_is_simple() == []
    @property
    def area(self):
        return (view_pos(unit+LINE_WIDTH, 0) if self.horizonal else view_pos(0, unit+LINE_WIDTH)) \
               if self.is_simple_or_has_to_be \
               else (view_pos(unit, 0) if self.horizonal else view_pos(0, unit)) 
    # @property
    # def area(self):
    #     return (view_pos(unit+LINE_WIDTH, 0) if self.horizonal else view_pos(0, unit+LINE_WIDTH))
    def fill(self):
        self.draw_progress.progress = self.area
        self.exist = True
        self.draw_progress.dcsp.on()
    def clear(self):
        self.draw_progress.progress = view_pos(0, 0)
        self.exist = False
        self.draw_progress.dcsp.off()
    # endregion
    # region near
    @property
    def left_obj(self):  return line(self.p1.left_obj,  self.p2.left_obj)
    @property
    def right_obj(self): return line(self.p1.right_obj, self.p2.right_obj)
    @property
    def up_obj(self):    return line(self.p1.up_obj,    self.p2.up_obj)
    @property
    def down_obj(self):  return line(self.p1.down_obj,  self.p2.down_obj)
    #endregion
all_square:dict[pos2, 'square'] = {}
class square:
    def __new__(cls, pos: pos2): # pos: left&up
        if pos in all_square: return all_square[pos]
        if pos.x >= a or pos.y >= a: return None
        if pos.x < 0 or pos.y < 0: return None
        return super().__new__(cls)
    def __init__(self, pos: pos2): # pos: left&up
        if pos in all_square: return
        self.pos = pos
        self.point = point(self.pos)
        self.content: square_content|None = None
        all_square[self.pos] = self
    def __hash__(self): return hash(self.point)
    @classmethod
    def by_point(cls, p: point):
        if p is None: return None
        return square(p.pos)
    @property
    def line_passed(self) -> int:
        f = lambda l: not l is None and l.exist
        return f(self.left_line) + f(self.right_line) + f(self.up_line) + f(self.down_line)
    def __repr__(self): return 'square' + repr(self.point)
    def __getnewargs__(self): return (self.pos, )
    def set_content(self, content: square_content): 
        # if type(content) != tuple:
        #     assert False
        # if not content[0] in (LPN, PI, SU, SR):
        #     assert False
        self.content = content
    # region part: line
    @property
    def left_line(self): return line(self.point, self.point.down_obj)
    @property
    def right_line(self): return self.left_line.right_obj
    @property
    def up_line(self): return line(self.point, self.point.right_obj)
    @property
    def down_line(self): return self.up_line.down_obj
    # endregion
    
    # region near obj
    @property
    def left_obj(self):  return square.by_point(self.point.left_obj)
    @property
    def right_obj(self): return square.by_point(self.point.right_obj)
    @property
    def up_obj(self):    return square.by_point(self.point.up_obj)
    @property
    def down_obj(self):  return square.by_point(self.point.down_obj)
    #endregion

    def near_samep(self) -> list[Self]:
        res = []
        if self.left_obj and not self.left_line.exist:   res.append(self.left_obj)
        if self.right_obj and not self.right_line.exist: res.append(self.right_obj)
        if self.up_obj and not self.up_line.exist:       res.append(self.up_obj)
        if self.down_obj and not self.down_line.exist:   res.append(self.down_obj)
        return res
    
    def near_samep_for_check(self) -> list[Self]:
        res = []
        if self.left_obj and not self.left_line.is_on():   res.append(self.left_obj)
        if self.right_obj and not self.right_line.is_on(): res.append(self.right_obj)
        if self.up_obj and not self.up_line.is_on():       res.append(self.up_obj)
        if self.down_obj and not self.down_line.is_on():   res.append(self.down_obj)
        return res
    @classmethod
    def set_by_a(cls, a):
        for x in range(a):
            for y in range(a):
                s = square(pos2(x, y))
                assert not s.left_line is None
                s.left_line; s.right_line; s.up_line; s.down_line
    @classmethod
    def all(cls): return all_square
    @classmethod
    def clear(cls): global all_square; all_square = {}
    @classmethod
    def set(cls, l): global all_square; all_square = l
# region puzzle draw
def draw_triangle(surface, A: view_pos, B: view_pos, C: view_pos, color):
    gfxdraw.aatrigon(surface, A.x, A.y, B.x, B.y, C.x, C.y, color)
    gfxdraw.filled_trigon(surface, A.x, A.y, B.x, B.y, C.x, C.y, color)
def _draw_radius_border_rect(color, pos:view_pos, width, height, surface):
    draw.rect(surface, color, (pos.x, pos.y, width, height), border_radius=RBR)


# puzzle_draw: dict[content_type, Callable[[Any, square, pygame.surface.Surface], None]] = {
#     LPN: LPN_draw,
#     PI: PI_draw,
#     SU: SU_draw,
#     SR: SR_draw
# }
def start_point_draw(surface):
    tmp = p2vpo(point_start, (-LINE_WIDTH*special_point_length, 0))
    draw.rect(surface, line_color['line_must_pass'], 
              (tmp[0], tmp[1], LINE_WIDTH*special_point_length, LINE_WIDTH))
def end_point_draw(surface):
    tmp = p2vpo(point_end, (0, 0))
    draw.rect(surface, line_color['line_must_pass'], 
              (tmp[0], tmp[1], LINE_WIDTH*special_point_length+LINE_WIDTH, LINE_WIDTH))
def main_draw(surface):
    surface.fill(BGC)
    # lts = []
    for l in line.all().values():
        # lts.append(l.type)
        l.draw(surface)
    start_point_draw(surface)
    end_point_draw(surface)
    for k in all_square:
        s = all_square[k]
        if s.content:
            # _content_type:cse.basic.poss_cls_sq = s.content[0]
            _content_type:cse.basic.poss_cls_sq = s.content
            _content_type.draw(s, unit, surface)
            # print(_content_type)
            # if not _content_type in puzzle_draw:
                # print('-_-continue')
                # continue
            # puzzle_draw[_content_type](s.content[1], s, surface)
    pygame.display.flip()
    print(Fore.YELLOW+'l_dprog_log_b')
    for k in all_line:
        l = all_line[k]
        if l.draw_progress.progress.length != 0:
            print(Fore.RED+repr(l)+'_'+repr(l.draw_progress)+Fore.RESET)
    print(Fore.YELLOW+'l_dprog_log_e')
# endregion
point_start: pos2 = None
point_end: pos2 = None
line_id = str
puzzle_square_type = dict[pos2, square_content]
puzzle_line_type = dict[line_id, line_type]
puzzle_type = tuple[puzzle_square_type, puzzle_line_type]
rectified_mouse_pos = None
def set_by_puzzle(puzzle: puzzle_type, p_start, p_end):
    'set square and line object by puzzle to draw and sth'
    # global point_start, point_end, decision_pos, now_line, mouse_reset_pos, dcs_point
    global point_start, point_end, rectified_mouse_pos, last_mouse_pos
    ps, pl = puzzle
    for s in ps:
        square(s).set_content(ps[s])
    for l in pl:
        line.by_id(l).set_type(pl[l])
    point_start = p_start
    point_end = p_end
    rectified_mouse_pos = p2vpo(p_start)
    pygame.mouse.set_pos(rectified_mouse_pos.to_tuple())
    am.set_dcsp(point(point_start))
set_visible = pygame.mouse.set_visible
set_grab = pygame.event.set_grab
get_grab = pygame.event.get_grab

def on_mouse_move(now_mouse_pos: view_pos):
    global rectified_mouse_pos
    now_line = am.get_nl()
    # TODO this may allow mouse get out of max movement, 
    # check it, like nmp = max(vec(nmp), vec(nmp)^0 * |max_movement|)
    print('on_mouse_move(nmp, rmp, dcsp, check_end)', 
          now_mouse_pos, 
          rectified_mouse_pos,
          repr(am.state.get('dcsp', None))+':'+repr(p2vpo(am.state.get('dcsp', None))), 
          end=' ')
    _d = now_mouse_pos - rectified_mouse_pos
    am.overflow_check(now_mouse_pos, rectified_mouse_pos, unit) # rectified_mouse_pos: last mouse pos
    print(now_mouse_pos)
    if point(now_line.pos1).collide(now_mouse_pos):
        am.at_turning(point(now_line.pos1), now_mouse_pos, unit, _d)
    elif point(now_line.pos2).collide(now_mouse_pos):
        am.at_turning(point(now_line.pos2), now_mouse_pos, unit, _d)
    prog = am.d2progress(am.rectify(now_mouse_pos))
    now_line: line = am.get_nl()
    assert not now_line is None
    # TODO draw fixed(won't out of area) but nmp may still | maybe fixed?
    now_line.draw_progress = prog
    # now_line.draw_progress = prog if prog <= now_line.area else now_line.area
    rectified_mouse_pos = now_mouse_pos
    if point(point_end).collide(now_mouse_pos):
        am.state['now_line'].fill()
        return 'END'

def event_loop() -> (Literal['EXIT', 'NEXT', 'MOUSE_UNLOCK', 'DRAW_UPDATE'] | None):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return 'EXIT'
        if event.type == pygame.locals.KEYDOWN:
            print('key_down')
            match event.key:
                case pygame.locals.K_ESCAPE:
                    return 'EXIT'
                case pygame.locals.K_TAB:
                    return 'NEXT'
                case pygame.locals.K_q:
                    return 'MOUSE_UNLOCK'
                case pygame.locals.K_r:
                    return 'RESTART'
        if event.type == pygame.locals.MOUSEMOTION:
            if any(pygame.mouse.get_pressed()):
                x, y = pygame.mouse.get_pos()
                res = on_mouse_move(view_pos(x, y))
                return 'END_CHECK' if res == 'END' else 'DRAW_UPDATE'
            # last_mouse_pos = now_mouse_pos
        pygame.mouse.set_pos(rectified_mouse_pos.to_tuple())
# loop()

# about mod loader
cse.basic.set_5basic_cls(point, line, square, pos2, view_pos)
cse.basic.set_5basic_func(set_a, p2vp, p2vpo, draw_triangle, _draw_radius_border_rect)