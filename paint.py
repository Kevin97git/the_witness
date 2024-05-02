import pygame
pygame.init()
import pygame.draw as draw
from pygame.locals import *
from collections import namedtuple
from functools import lru_cache
from typing import List, Any, Self
from copy import copy
from numpy import ndarray
import numpy as np
import sys

import config_save_error as cse
config = cse.get_config()

vec2 = namedtuple('vec2', 'x y')
# view_vec = namedtuple('view_vec', 'x y')
class view_vec(namedtuple('view_vec_super', 'x y')):
    __slots__ = ()
    def __sub__(self, other):
        return view_vec(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        return view_vec(self.x + other.x, self.y + other.y)
    def __mul__(self, other):
        return view_vec(self.x * other, self.y * other)
    def to_tuple(self):
        return (self.x, self.y)
'''
O ---- x
|
|
y
'''
wwidth = config["width"]
wheight = config["height"]
ud_bording = config["up_down_bording"]
LINE_WIDTH = config["line_width"]
lr_bording = int((wwidth - (wheight - ud_bording*2)) / 2)
view_pos_0_0:view_vec = view_vec(x=ud_bording, y=ud_bording)
public_surface = pygame.display.set_mode(size=(wwidth, wheight))
main_clock = pygame.time.Clock()
unit = 60
a:int = -1
def set_a(_a: int):
    global a, unit
    a = _a
    unit = int(((wheight - ud_bording*2) - (a + 1) * LINE_WIDTH) / a)

#const
A2C = 'able_to_cross'
line_color = {
    A2C: (144, 144, 144),
    -1: (255, 255, 255),
    1: (50, 50, 50)
}
def pos_to_view_pos(pos:vec2):
    return view_vec(
        x=view_pos_0_0.x+pos.x*unit+pos.x*LINE_WIDTH+LINE_WIDTH,
        y=view_pos_0_0.y+pos.y*unit+pos.y*LINE_WIDTH+LINE_WIDTH
    )
p2vp = pos_to_view_pos
shape_length_minimum = config["shape_length_minimum"]

# def view_vec_sub(a, b):
#     return view_vec(a.x - b.x, a.y - b.y)
all_point = {}
class point:
    def __new__(cls, pos: vec2):
        if pos in all_point:
            return all_point[pos]
        if pos.x > a or pos.y > a:
            return None
        if pos.x < 0 or pos.y < 0:
            return None
        return super().__new__(cls)
    def __init__(self, pos: vec2):
        if pos in all_point:
            return
        self.x = pos.x
        self.y = pos.y
        self.pos = pos
        self.passed = False
        all_point[pos] = self
    @property
    def on(self):
        self.passed = True
        return self
    @property
    def off(self):
        self.passed = False
        return self
    @lru_cache
    def left_obj(self):
        return point(vec2(self.x - 1, self.y))
    @lru_cache
    def right_obj(self):
        return point(vec2(self.x + 1, self.y))
    @lru_cache
    def up_obj(self):
        return point(vec2(self.x, self.y - 1))
    @lru_cache
    def down_obj(self):
        return point(vec2(self.x, self.y + 1))
    def __repr__(self):
        return f'({self.pos.x}, {self.pos.y})'
all_line = {}
class line:
    def __new__(cls, p1: point, p2: point):
        if p1 is None or p2 is None:
            # print('none')
            return None
        _id = f'{p1};{p2}'
        if _id in all_line:
            # print('in_list')
            return all_line[_id]
        if p1.x != p2.x and p1.y != p2.y:
            cse.raise_error('class line, __init__, unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
        if p1 == p2:
            cse.raise_error('class line, __init__, unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
        # print('new')
        if p1.x > p2.x: assert False
        return super().__new__(cls)
    def __init__(self, p1: point, p2: point):
        # p1 left or up
        self.id = f'{p1};{p2}'
        if self.id in all_line:
            return
        # print('init')
        self.p1 = p1
        self.pos1 = p1.pos
        self.p2 = p2
        self.pos2 = p2.pos
        self.type = -1
        self.exist = False
        self.horizonal = p1.y == p2.y
        all_line[self.id] = self
    @classmethod
    def untidy(cls, p1: point, p2: point):
        if p1.x < p2.x or p1.y < p2.y:
            return cls(p1, p2)
        if p1.x > p2.x or p1.y > p2.y:
            return cls(p2, p1)
        assert False
    @classmethod
    def all(cls): return all_line
    
    @classmethod
    def from_to(cls, p1: point, p2: point):
        if p1.x == p2.x:
            for i in range(0, p2.y - p1.y):
                line(point(vec2(p1.x, p1.y+i)), point(vec2(p1.x, p1.y+i+1))).on
        elif p1.y == p2.y:
            for i in range(0, p2.x - p1.x):
                line(point(vec2(p1.x+i, p1.y)), point(vec2(p1.x+i+1, p1.y))).on
        else:
            cse.raise_error('class line, classmethod "from_to", unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
    @classmethod
    def from_to_untidy(cls, p1: point, p2: point):
        if p1.x < p2.x or p1.y < p2.y:
            return cls.from_to(p1, p2)
        if p1.x > p2.x or p1.y > p2.y:
            return cls.from_to(p2, p1)
        assert False
    
    @property
    def draw_offset(self):
        # if self.horizonal:
        #     return view_vec(LINE_WIDTH, 0)
        return view_vec(LINE_WIDTH, LINE_WIDTH)
    def draw(self):
        draw.line(public_surface, line_color[self.type], 
                  (p2vp(self.pos1) - self.draw_offset).to_tuple(), 
                  (p2vp(self.pos2) - self.draw_offset).to_tuple(),
                  LINE_WIDTH)
    def draw_by(self, color):
        draw.line(public_surface, color, 
                  (p2vp(self.pos1) - self.draw_offset).to_tuple(), 
                  (p2vp(self.pos2) - self.draw_offset).to_tuple(),
                  LINE_WIDTH)
    @property
    def on(self):
        self.exist = True
        self.p1.on
        self.p2.on
        return self
    @property
    def off(self):
        # print('off')
        self.exist = False
        # print(self.exist)
        # print(all_line[self.id].exist)
        self.p1.off
        self.p2.off
        return self
    def set(self, type):
        self.type = type
    def __repr__(self):
        return self.id+('T' if self.exist else 'F')
    #region near
    @lru_cache
    def left_obj(self):
        return line(self.p1.left_obj(), self.p2.left_obj())
    @lru_cache
    def right_obj(self):
        return line(self.p1.right_obj(), self.p2.right_obj())
    @lru_cache
    def up_obj(self):
        return line(self.p1.up_obj(), self.p2.up_obj())
    @lru_cache
    def down_obj(self):
        return line(self.p1.down_obj(), self.p2.down_obj())
    #endregion
all_square = {}
class square:
    def __new__(cls, pos: vec2): # pos: left&up
        if pos in all_square:
            return all_square[pos]
        if pos.x >= a or pos.y >= a:
            return None
        if pos.x < 0 or pos.y < 0:
            return None
        return super().__new__(cls)
    def __init__(self, pos: vec2): # pos: left&up
        if pos in all_square: return
        self.pos = pos
        self.point = point(self.pos)
        all_square[self.pos] = self
    @classmethod
    def by_point(cls, p: point):
        if p is None: return None
        return square(p.pos)
    @property
    def line_passed(self):
        return self.left_line().exist + self.right_line().exist + self.up_line().exist + self.down_line().exist
    def __repr__(self):
        return 'square' + repr(self.point)
    # region part: line
    @lru_cache
    def left_line(self):
        return line(self.point, self.point.down_obj())
    @lru_cache
    def right_line(self):
        return self.left_line().right_obj()
    # @lru_cache
    def up_line(self):
        return line(self.point, self.point.right_obj())
    @lru_cache
    def down_line(self):
        return self.up_line().down_obj()
    # endregion
    
    # region near obj
    @lru_cache
    def left_obj(self):
        return square.by_point(self.point.left_obj())
    @lru_cache
    def right_obj(self):
        return square.by_point(self.point.right_obj())
    @lru_cache
    def up_obj(self):
        return square.by_point(self.point.up_obj())
    @lru_cache
    def down_obj(self):
        return square.by_point(self.point.down_obj())
    #endregion

    def near_samep(self):
        # print('near_samp')
        # print(list(all_line.values()))
        res = []
        if self.left_obj():
            if not self.left_line().exist:
                res.append(self.left_obj())
        if self.right_obj():
            if not self.right_line().exist:
                res.append(self.right_obj())
        if self.up_obj():
            if not self.up_line().exist:
                res.append(self.up_obj())
        if self.down_obj():
            if not self.down_line().exist:
                res.append(self.down_obj())
        print('res', len(res))
        return res
    @classmethod
    def set_by_a(cls, a):
        for x in range(a):
            for y in range(a):
                s = square(vec2(x, y))
                if s.left_line() is None:
                    assert False
                s.right_line()
                s.up_line()
                s.down_line()
    @classmethod
    def all(cls):
        return all_square


shapes: List[List[List[int]]] = []
config_shapes: List[str] = config["shapes"]
for s in config_shapes:
    l = []
    s = s.split('_')
    for row in s:
        sub_l = []
        for b in row:
            if b == 'T':  sub_l.append(1)
            else: sub_l.append(0)
        l.append(sub_l)
    shapes.append(np.array(l))
class once:
    def __init__(self, obj):
        self.obj = obj
        self.available = True
    def use(self):
        self.available = False
    def __repr__(self):
        return repr(self.obj)
    
# rotate = lambda l:np.array([[l[-j-1, i] for j in range(l.shape[0])] for i in range(l.shape[1])])
rotate = lambda a:a.transpose()[::-1]
class shape:
    @classmethod
    def rotate_the_same(cls, pattern):
        rtte = rotate(pattern)
        if pattern.shape == rtte.shape and (rtte == pattern).all(): return True
        return False
    def __init__(self, pattern, rotate_time=0):#clockwise
        self.pattern = pattern
        self.rotate_time = rotate_time
        self.rotated = pattern
        for _ in range(rotate_time): self.rotated = rotate(self.rotated)
    
    def to_grid(self, offset_x, offset_y):
        res = np.zeros((a, a))
        res[offset_y: offset_y+self.height, offset_x: offset_x+self.width] = self.rotated
        return res
    


    # @property
    # def width(self):
    #     return len(self.rotated[0])
    @property
    def width(self):
        return self.rotated.shape[1]
    @property
    def height(self):
        return self.rotated.shape[0]
    def __repr__(self):
        return '_'.join([''.join(['T' if self.pattern[y, x] else 'F' for x in range(self.pattern.shape[1])]) for y in range(self.pattern.shape[0])])+str(self.rotate_time)
def all_shape():
    res = []
    for _s in shapes:
        for rt in range(1 if shape.rotate_the_same(_s) else 4):
            res.append(shape(_s, rt))
    return res
class grid:
    def __init__(self, part:list):
        self.l = [[(1 if square(vec2(x, y)) in part else 0) for x in range(a)] for y in range(a)]
        self.l:ndarray = np.array(self.l, int)
        # print(self.l)
    @classmethod
    def by_l(cls, l):
        res = super().__new__(cls)
        res.l = l
        return res
    # def __sub__(self, oth):
    #     return grid.by_l([[(self.l[y][x] - oth[y][x]) for x in range(a)] for y in range(a)])
    def __sub__(self, oth:ndarray):
        return self.l - oth
    # def n_include(self, what, target):
    #     for e in what:
    #         if target in e: return False
    #     return True
    def n_include(self, what, target):
        return what[what == target].shape == (0,)
    def match(self, s: shape) -> tuple[list[tuple[shape, vec2, Self]], list[tuple[shape, vec2]]]:
        res = []
        rprob = []
        for y in range(a + 1 - s.height):
            for x in range(a + 1 - s.width):
                se = self - s.as_grid(x, y)
                if se[se == -1].shape == (0,): 
                    res.append([(s, vec2(x, y), grid.by_l(se))])
                    rprob.append((s, vec2(x, y)))

        return (res, rprob)
    def match_prefix(self, s: shape, prefix:list):
        res = []
        for y in range(a + 1 - s.height):
            for x in range(a + 1 - s.width):
                se = self - (s.to_grid(x, y))
                if se[se == -1].shape == (0,): 
                    res.append(prefix + [(s, vec2(x, y), grid.by_l(se))])
        return res
    def one_num(self):
        return self.l.sum()
    # @lru_cache
    def __repr__(self):
        return '_'.join([''.join(['T' if self.l[y, x] == 1 else 'F' for x in range(a)]) for y in range(a)])
    
    # def item(self):
    #     res = []
    #     for y in self.l:
    #         for x in y:
    #             if not x in res: res.append(x)
    #     return res

    # @lru_cache
    # def __ne__(self, other):
    #     return self.__repr__() != repr(other)
def _draw_radius_border_rect(color, pos:view_vec, width, height):
    draw.rect(public_surface, color, (pos.x, pos.y, width, height), 20)
def LPN_draw():
    pass
PI_color = config["part_mark_color"]
SIS = config["single_icon_size"]
def PI_draw(arg, s:square):
    _draw_radius_border_rect(PI_color[str(arg)], p2vp(s.pos) - view_vec(unit, unit)*(SIS / 2), SIS, SIS)
# probabilities include const
LPN = 'line_passed_number: '
PI = 'part_index: '
puzzle_draw = {
    LPN: LPN_draw,
    PI: PI_draw
}

def main_draw():
    public_surface.fill((0, 0, 0))
    for l in line.all().values():
        l.draw_by(line_color[1])
    for l in line.all().values():
        if l.exist:
            l.type = -1
            l.draw()
    pygame.display.update()
def loop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                print('key_down')
                match event.key:
                    case K_ESCAPE:
                        sys.exit()
        main_draw()
        main_clock.tick(30)


# loop()