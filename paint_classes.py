import pygame
pygame.init()
import pygame.draw as draw
import pygame.gfxdraw as gfxdraw
import pygame.locals
from pygame.display import set_caption
from collections import namedtuple
from functools import lru_cache
from typing import List, Any, Self, Literal, Callable
from copy import copy
from numpy import ndarray
import numpy as np
import math
import sys

import config_save_error as cse
from constant_type import *

# vec2 = namedtuple('vec2', 'x y')
class vec2(namedtuple('vec2_super', 'x y')):
    __slots__ = ()
    def __repr__(self):
        return f'v({self.x}, {self.y})'
# view_vec = namedtuple('view_vec', 'x y')
class view_vec(namedtuple('view_vec_super', 'x y')):
    __slots__ = ()
    def __new__(cls, x, y):
        return super().__new__(cls, int(x), int(y))
    def __sub__(self, other):
        return view_vec(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        return view_vec(self.x + other.x, self.y + other.y)
    def __mul__(self, other):
        return view_vec(self.x * other, self.y * other)
    def to_tuple(self):
        return (self.x, self.y)
    @property
    def slope(self):
        return self.y / self.x if self.x != 0 else math.inf
'''
O ---- x
|
|
y
'''
content_0_0:view_vec = view_vec(x=lr_border, y=tb_border)
def get_surface():
    return pygame.display.set_mode(size=(wwidth, wheight), 
                                   flags=0)
main_clock = pygame.time.Clock()
unit = -1
a:int = -1
def set_a(_a: int):
    global a, unit
    a = _a
    unit = int(((wheight - tb_border*2) - (a + 1) * LINE_WIDTH) / a)

def pos_to_view_pos(pos:vec2):
    return view_vec(
        x=content_0_0.x+pos.x*unit+pos.x*LINE_WIDTH+LINE_WIDTH,
        y=content_0_0.y+pos.y*unit+pos.y*LINE_WIDTH+LINE_WIDTH
    )
def pos_to_view_pos_offset(pos:vec2, offset: tuple[int, int]=(0, 0)): # for line.draw
    return view_vec(
        x=content_0_0.x+pos.x*unit+pos.x*LINE_WIDTH + int(offset[0]),
        y=content_0_0.y+pos.y*unit+pos.y*LINE_WIDTH + int(offset[1])
    )
p2vp = pos_to_view_pos
p2vpo = pos_to_view_pos_offset

square_content = tuple[Literal['line_passed_number: '], int] \
                 | tuple[Literal['part_index: '], int] \
                 | tuple[Literal['shape_rotatable: '], 'shape'] \
                 | tuple[Literal['shape_unrotatable: '], 'shape']
content_type = Literal['line_passed_number: ', 'part_index: ', 'shape_rotatable: ', 'shape_unrotatable: ']
line_type = Literal['line_must_pass'] | Literal['line_cannot_pass'] | Literal['simple']
#debug
next_id = 0
def get_id():
    global next_id
    return (next_id := next_id+1)

def draw_line(surface, color, start_pos, end_pos, width, horizon) -> pygame.rect.Rect:
    return draw.rect(surface, color, 
                     (start_pos[0], start_pos[1], end_pos[0] - start_pos[0] + width, width)
                     if horizon else (start_pos[0], start_pos[1], width, end_pos[1] - start_pos[1] + width))

def property_cache(f):
    @property
    @lru_cache
    def res(*args, **kwargs):
        return f(*args, **kwargs)
    return res
all_point:dict[vec2, 'point'] = {}
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
        self.x, self.y = pos
        self.pos = pos
        self.passed = False
        all_point[pos] = self
    def on(self): self.passed = True; return self
    def off(self): self.passed = False; return self
    def __repr__(self): return f'({self.pos.x}, {self.pos.y})'
    def __getnewargs__(self): return self.pos
    @classmethod
    def all(cls): return all_point
    @classmethod
    def clear(cls): global all_point; all_point = {}
    @classmethod
    def set(cls, l): global all_point; all_point = l
    def collide(self, pos: view_vec):
        d = p2vp(self.pos) - pos
        return math.hypot(d.x, d.y) < MCR * unit
    # region near obj
    @property_cache
    def left_obj(self):  return point(vec2(self.x - 1, self.y))
    @property_cache
    def right_obj(self): return point(vec2(self.x + 1, self.y))
    @property_cache
    def up_obj(self):    return point(vec2(self.x, self.y - 1))
    @property_cache
    def down_obj(self):  return point(vec2(self.x, self.y + 1))
    # endregion
    def near_line(self): return [
        line(self.up_obj, self), line(self, self.down_obj), 
        line(self.left_obj, self), line(self, self.right_obj)
    ]
    def near_line_is_simple(self): return [l for l in self.near_line() if l and l.type == 'simple']
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
        self.type: line_type = 'simple'
        self.draw_progress: int = 0
        self.exist = False
        self.horizonal = (p1.y == p2.y)
        all_line[self.id] = self
    @classmethod
    def untidy(cls, p1: point, p2: point):
        if p1.x < p2.x or p1.y < p2.y: return cls(p1, p2)
        if p1.x > p2.x or p1.y > p2.y: return cls(p2, p1)
        assert False
    @classmethod
    def by_id(cls, _id):
        return all_line[_id]
    @classmethod
    def all(cls): return all_line
    @classmethod
    def clear(cls): global all_line; all_line = {}
    @classmethod
    def set(cls, l): global all_line; all_line = l
    @classmethod
    def classify(cls):
        on: list[Self] = []
        off: list[Self] = []
        for k in all_line:
            if all_line[k].exist: on.append(all_line[k])
            else: off.append(all_line[k])
        return on, off
    
    @classmethod
    def from_to(cls, p1: point, p2: point):
        if p1.x == p2.x:
            for i in range(0, p2.y - p1.y):
                line(point(vec2(p1.x, p1.y+i)), point(vec2(p1.x, p1.y+i+1))).on()
        elif p1.y == p2.y:
            for i in range(0, p2.x - p1.x):
                line(point(vec2(p1.x+i, p1.y)), point(vec2(p1.x+i+1, p1.y))).on()
        else:
            cse.raise_error('class line, classmethod "from_to", unexpected values of arguments p1, p2: ' + str(p1) + ';' + str(p2))
    @classmethod
    def from_to_untidy(cls, p1: point, p2: point):
        if p1.x < p2.x or p1.y < p2.y: return cls.from_to(p1, p2)
        if p1.x > p2.x or p1.y > p2.y: return cls.from_to(p2, p1)
        assert False
    
    @property_cache
    def draw_offset(self):
        if self.type == 'simple': return (0, 0)
        if point(self.pos1).near_line_is_simple() == []:
            return (0, 0)
        return (LINE_WIDTH, 0) if self.horizonal else (0, LINE_WIDTH)
    @property_cache
    def progress_offset(self):
        return (self.draw_progress - LINE_WIDTH, 0) \
               if self.horizonal                    \
               else (0, self.draw_progress - LINE_WIDTH)
    def draw(self, surface):
        draw_line(surface, line_color[self.type], 
                  p2vpo(self.pos1, self.draw_offset).to_tuple(), 
                  p2vpo(self.pos2).to_tuple(),
                  LINE_WIDTH, self.horizonal)
        draw_line(surface, line_color['draw'], 
                  p2vpo(self.pos1, self.draw_offset).to_tuple(), 
                  p2vpo(self.pos1, self.progress_offset).to_tuple(),
                  LINE_WIDTH, self.horizonal)
        print('--------', self.draw_progress, '--------')
    def draw_by(self, color, surface):
        assert False
        draw_line(surface, color, 
                  p2vpo(self.pos1, self.draw_offset).to_tuple(), 
                  p2vpo(self.pos2).to_tuple(),
                  LINE_WIDTH, self.horizonal)
    def on(self):
        self.exist = True
        self.p1.on()
        self.p2.on()
        return self
    def off(self):
        self.exist = False
        self.p1.off()
        self.p2.off()
        return self
    def set_type(self, type): self.type = type
    def __repr__(self): return self.id+('T' if self.exist else 'F')
    def __getnewargs__(self): return (self.p1, self.p2)
    @classmethod
    def clear_progress(cls):
        for l in all_line:
            all_line[l].draw_progress = 0
    def right_is_end(self):
        if self.pos2 == point_end:
            return True
        return False
    def set_progress(self, 
                     direction:Literal['up']|Literal['down']|Literal['left']|Literal['right'], 
                     num) -> Literal[1]|Literal[-1]|Self:
        if self.type == 'line_cannot_pass': return -1
        self.draw_progress += num
        if self.draw_progress <= 0:
            self.draw_progress = 0
            if direction == 'up':    return self.up_obj
            if direction == 'down':  return self.down_obj
            if direction == 'left':  return self.left_obj
            if direction == 'right': return self.right_obj
            assert False
        if self.draw_progress >= unit + LINE_WIDTH:
            self.draw_progress = unit + LINE_WIDTH
            if direction == 'up':    return self.up_obj
            if direction == 'down':  return self.down_obj
            if direction == 'left':  return self.left_obj
            if direction == 'right': return self.right_obj
            assert False
        return 1

    #region near
    @property_cache
    def left_obj(self):  return line(self.p1.left_obj,  self.p2.left_obj)
    @property_cache
    def right_obj(self): return line(self.p1.right_obj, self.p2.right_obj)
    @property_cache
    def up_obj(self):    return line(self.p1.up_obj,    self.p2.up_obj)
    @property_cache
    def down_obj(self):  return line(self.p1.down_obj,  self.p2.down_obj)
    #endregion
all_square:dict[vec2, 'square'] = {}
class square:
    def __new__(cls, pos: vec2): # pos: left&up
        if pos in all_square: return all_square[pos]
        if pos.x >= a or pos.y >= a: return None
        if pos.x < 0 or pos.y < 0: return None
        return super().__new__(cls)
    def __init__(self, pos: vec2): # pos: left&up
        if pos in all_square: return
        self.pos = pos
        self.point = point(self.pos)
        self.content: square_content|None = None
        all_square[self.pos] = self
    @classmethod
    def by_point(cls, p: point):
        if p is None: return None
        return square(p.pos)
    @property
    def line_passed(self) -> int:
        return self.left_line.exist + self.right_line.exist + self.up_line.exist + self.down_line.exist
    def __repr__(self): return 'square' + repr(self.point)
    def __getnewargs__(self): return (self.pos, )
    def set_content(self, content: square_content): 
        if type(content) != tuple:
            assert False
        if not content[0] in (LPN, PI, SU, SR):
            assert False
        self.content = content
    # region part: line
    @property_cache
    def left_line(self): return line(self.point, self.point.down_obj)
    @property_cache
    def right_line(self): return self.left_line.right_obj
    @property_cache
    def up_line(self): return line(self.point, self.point.right_obj)
    @property_cache
    def down_line(self): return self.up_line.down_obj
    # endregion
    
    # region near obj
    @property_cache
    def left_obj(self):  return square.by_point(self.point.left_obj)
    @property_cache
    def right_obj(self): return square.by_point(self.point.right_obj)
    @property_cache
    def up_obj(self):    return square.by_point(self.point.up_obj)
    @property_cache
    def down_obj(self):  return square.by_point(self.point.down_obj)
    #endregion

    def near_samep(self) -> list[Self]:
        res = []
        if self.left_obj and not self.left_line.exist:   res.append(self.left_obj)
        if self.right_obj and not self.right_line.exist: res.append(self.right_obj)
        if self.up_obj and not self.up_line.exist:       res.append(self.up_obj)
        if self.down_obj and not self.down_line.exist:   res.append(self.down_obj)
        return res
    @classmethod
    def set_by_a(cls, a):
        for x in range(a):
            for y in range(a):
                s = square(vec2(x, y))
                assert not s.left_line is None
                s.left_line; s.right_line; s.up_line; s.down_line
    @classmethod
    def all(cls): return all_square
    @classmethod
    def clear(cls): global all_square; all_square = {}
    @classmethod
    def set(cls, l): global all_square; all_square = l
    

shapes: List[List[List[int]]] = []
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
        if type(obj) != tuple:
            assert False
        self.obj = obj
        self.available = True
        self.id = get_id()
    def use(self):
        self.available = False
    def __repr__(self):
        assert type(self.obj) != grid
        return str(self.id)+repr(self.obj)
    
# rotate = lambda l:np.array([[l[-j-1, i] for j in range(l.shape[0])] for i in range(l.shape[1])])
rotate = lambda a:a.transpose()[::-1]
class shape:
    @classmethod
    def rotate_the_same(cls, pattern):
        rtte = rotate(pattern)
        if pattern.shape == rtte.shape and (rtte == pattern).all(): return True
        return False
    def __init__(self, pattern: ndarray, rotate_time=0):#clockwise
        self.pattern = pattern
        self.rotate_time = rotate_time
        self.rotated: ndarray = pattern
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
        return '_'.join([''.join([
            'T' if self.pattern[y, x] else 'F' for x in range(self.pattern.shape[1])
        ]) for y in range(self.pattern.shape[0])])+str(self.rotate_time)
    @classmethod
    def all(cls):
        res = []
        for _s in shapes:
            for rt in range(1 if cls.rotate_the_same(_s) else 4):
                res.append(cls(_s, rt))
        return res
shape_prob_type = tuple[shape, vec2]
class grid:
    def __init__(self, part:list):
        self.l = [[(1 if square(vec2(x, y)) in part else 0) for x in range(a)] for y in range(a)]
        self.l:ndarray = np.array(self.l, int)
    @classmethod
    def by_l(cls, l):
        res = super().__new__(cls)
        res.l = l
        return res
    def __sub__(self, oth:ndarray): return self.l - oth
    def n_include(self, what, target): return what[what == target].shape == (0,)
    def match(self, s: shape) -> tuple[list[list[tuple[shape, vec2, Self]]], list[tuple[shape, vec2]]]:
        res = []
        rprob = []
        for y in range(a + 1 - s.height):
            for x in range(a + 1 - s.width):
                se = self - s.to_grid(x, y)
                if se[se == -1].shape == (0,): 
                    res.append([(s, vec2(x, y), grid.by_l(se))])
                    rprob.append((s, vec2(x, y)))

        return (res, rprob)
    def match_prefix(self, s: shape_prob_type, prefix:list) -> tuple[list[list[tuple[shape, vec2, Self]]], list[tuple[shape, vec2]]]:
        res = []
        rprob = []
        se = self - (s[0].to_grid(s[1].x, s[1].y))
        if se[se == -1].shape == (0,): 
            res.append(prefix + [(s[0], s[1], grid.by_l(se))])
            rprob.append((s[0], s[1]))
        return (res, rprob)
    def one_num(self): return self.l.sum()
    # @lru_cache
    def __repr__(self):
        return '_'.join([''.join(['T' if self.l[y, x] == 1 else 'F' for x in range(a)]) for y in range(a)])
def draw_triangle(surface, A: view_vec, B: view_vec, C: view_vec, color):
    gfxdraw.aatrigon(surface, A.x, A.y, B.x, B.y, C.x, C.y, color)
    gfxdraw.filled_trigon(surface, A.x, A.y, B.x, B.y, C.x, C.y, color)
def _draw_radius_border_rect(color, pos:view_vec, width, height, surface):
    draw.rect(surface, color, (pos.x, pos.y, width, height), border_radius=RBR)
def LPN_draw(arg:int, s:square, surface: pygame.surface.Surface):
    # scale_surface.fill(BGC)
    O = p2vp(s.pos)
    # O = view_vec(0, 0)
    # scaler = 10000 / unit
    scaler = 1
    u = unit / SSN * scaler
    d = IIDLPN * unit * scaler
    uad = view_vec(u + d, 0)
    match arg:
        case 1:
            A1 = O + view_vec(0.5 * u * SSN, GL1 * u * SSN)
            B1 = O + view_vec(GL1 * u * SSN, GL2 * u * SSN)
            C1 = O + view_vec(GL2 * u * SSN, GL2 * u * SSN)
            draw_triangle(surface, A1, B1, C1, LPN_color)
        case 2:
            A1 = O + view_vec(2 * u - d / 2, GL1 * u * SSN)
            B1 = O + view_vec(1.5 * u - d / 2, GL2 * u * SSN)
            C1 = O + view_vec(2.5 * u - d / 2, GL2 * u * SSN)
            draw_triangle(surface, A1, B1, C1, LPN_color)
            A2 = A1 + uad
            B2 = B1 + uad
            C2 = C1 + uad
            draw_triangle(surface, A2, B2, C2, LPN_color)
        case 3:
            A1 = O + view_vec(0.5 * u * SSN, 1.5 * u - d / 2)
            B1 = O + view_vec(GL1 * u * SSN, 2.5 * u - d / 2)
            C1 = O + view_vec(GL2 * u * SSN, 2.5 * u - d / 2)
            draw_triangle(surface, A1, B1, C1, LPN_color)
            A2 = O + view_vec(2 * u - d / 2, GL1 * u * SSN + u / 2 + d / 2)
            B2 = O + view_vec(1.5 * u - d / 2, GL1 * u * SSN + 1.5 * u + d / 2)
            C2 = O + view_vec(2.5 * u - d / 2, GL1 * u * SSN + 1.5 * u + d / 2)
            draw_triangle(surface, A2, B2, C2, LPN_color)
            A3 = A2 + uad
            B3 = B2 + uad
            C3 = C2 + uad
            draw_triangle(surface, A3, B3, C3, LPN_color)
        case 4: assert False
    # res = surface_scale(scale_surface)
    # surface.blit(res, p2vp(s.pos))
def PI_draw(arg:int, s:square, surface):
    print('pi_draw')
    _draw_radius_border_rect(PI_color[arg], 
        p2vpo(s.pos, ((1-SIS)*unit/2+LINE_WIDTH, (1-SIS)*unit/2+LINE_WIDTH)), 
        SIS*unit, SIS*unit, surface)
def SU_draw(arg: shape, s:square, surface):
    row, col = arg.rotated.shape
    d = IIDS * unit
    u = unit / SSN
    w = row * u - d
    h = col * u - d
    t = (unit - h) / 2
    l = (unit - w) / 2
    O = p2vp(s.pos)
    for y in range(col):
        for x in range(row):
            if arg.rotated[x, y]:
                draw.rect(surface, ISUC, 
                        (O.x+l+x*u, 
                        O.y+t+y*u, 
                        u-d, 
                        u-d))
def SR_draw(arg, s:square, surface):
    row, col = arg.rotated.shape
    d = IIDS * unit
    u = unit / SSN
    # ISRA => b, pi/2-ISRA => a, 90=>c=u
    # b/c = sin(ISRA)
    # b = c sin(ISRA) = u sin(ISRA)
    # a/c = cos(ISRA)
    # a = c cos(ISRA) = u cos(ISRA)
    b = (u-d) * ISRA_sin
    a = (u-d) * ISRA_cos
    w = row * u - d
    h = col * u - d
    t = (unit - h) / 2
    l = (unit - w) / 2
    O = p2vp(s.pos)
    for y in range(col):
        for x in range(row):
            if arg.rotated[x, y]:
                P1 = view_vec(O.x+l+x*u, O.y+t+y*u)
                P2 = P1 + view_vec(b, a)
                P3 = P2 + view_vec(a, -b)
                P4 = P1 + view_vec(a, -b)
                gfxdraw.aapolygon(surface, (P1, P2, P3, P4), ISRC)
                gfxdraw.filled_polygon(surface, (P1, P2, P3, P4), ISRC)
puzzle_draw: dict[content_type, Callable[[Any, square, pygame.surface.Surface], None]] = {
    LPN: LPN_draw,
    PI: PI_draw,
    SU: SU_draw,
    SR: SR_draw
}
point_start: vec2 = None
point_end: vec2 = None
line_id = str
puzzle_square_type = dict[vec2, square_content]
puzzle_line_type = dict[line_id, line_type]
puzzle_type = tuple[puzzle_square_type, puzzle_line_type]
def set_by_puzzle(puzzle: puzzle_type, p_start, p_end):
    global point_start, point_end
    ps, pl = puzzle
    for s in ps:
        square(s).set_content(ps[s])
    for l in pl:
        line.by_id(l).set_type(pl[l])
    point_start = p_start
    point_end = p_end
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
            _content_type = s.content[0]
            print(_content_type)
            if not _content_type in puzzle_draw:
                print('-_-continue')
                continue
            puzzle_draw[_content_type](s.content[1], s, surface)
    pygame.display.flip()
# last_mouse_pos = view_vec(0, 0)
set_visible = pygame.mouse.set_visible
set_grab = pygame.event.set_grab
get_grab = pygame.event.get_grab
last_mouse_pos = content_0_0 + view_vec(LINE_WIDTH/2, LINE_WIDTH/2)
direction: Literal['horizonal']|Literal['vertical']|None = None
now_line: line = None
def event_loop():
    global last_mouse_pos, direction, now_line
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
        if event.type == pygame.locals.MOUSEMOTION:
            if any(pygame.mouse.get_pressed()):

                x, y = pygame.mouse.get_pos()
                now_mouse_pos = view_vec(x, y)
                d = now_mouse_pos - last_mouse_pos
                for p in all_point:
                    if all_point[p].collide(now_mouse_pos): # at turning
                        print('at')
                        if d.slope < MMDA: # horizonal
                            last_mouse_pos += view_vec(d.x, 0)
                            direction = 'horizonal'
                            progress = d.x
                            if now_line is None:
                                now_line = line(point(point_start), point(point_start).right_obj)
                        elif d.slope > (1 / MMDA): # vertical
                            last_mouse_pos += view_vec(0, d.y)
                            direction = 'vertical'
                            progress = d.y
                            if now_line is None:
                                if progress > 0:
                                    now_line = line(point(point_start), point(point_start).down_obj)
                                else:
                                    now_line = line(point(point_start), point(point_start).up_obj)
                        else: print('miss', end=''); continue
                        print('prog:', progress)
                        print('d: ', d)
                        break
                else: # not at turning
                    print('=', end='')
                    if direction == 'horizonal':
                        last_mouse_pos += view_vec(d.x, 0)
                        progress = d.x
                    elif direction == 'vertical':
                        last_mouse_pos += view_vec(0, d.y)
                        progress = d.y
                res = now_line.set_progress(
                    ('up' if progress < 0 else 'down')
                    if direction=='horizonal'
                    else ('left' if progress < 0 else 'right'), 
                progress)
                if res == 1: # work well
                    pass
                elif res == -1: # line cannot pass
                    pass
                elif res: # line
                    now_line = res
                else: # not exist
                    if now_line.right_is_end(): return 'END'

            # last_mouse_pos = now_mouse_pos
        pygame.mouse.set_pos(last_mouse_pos)

# loop()