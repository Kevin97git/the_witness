from . import basic
from .basic import config, once, cache, pos2, view_pos, square, p2vp, cse
import numpy as np
from numpy import ndarray
from copy import copy
from pygame import gfxdraw, draw
list_shapes: list[list[list[int]]] = []
# config_shapes: list[str] = config["shapes"]
config_shapes: list[str] = config.shapes
# init
for s in config_shapes:
    l = []
    s = s.split('_')
    for row in s:
        sub_l = []
        for b in row:
            if b == 'T':  sub_l.append(1)
            else: sub_l.append(0)
        l.append(sub_l)
    list_shapes.append(np.array(l))
global_rand = None
    
# rotate = lambda l:np.array([[l[-j-1, i] for j in range(l.shape[0])] for i in range(l.shape[1])])
rotate = lambda a:a.transpose()[::-1]
class shape:
    @classmethod
    def rotate_the_same(cls, pattern):
        rtte = rotate(pattern) #rotate end pattern
        if pattern.shape == rtte.shape and (rtte == pattern).all(): return True
        return False
    def __init__(self, pattern: ndarray, rotate_time=0):#clockwise
        self.pattern = pattern
        self.rotate_time = rotate_time
        self.rotated: ndarray = pattern
        for _ in range(rotate_time): self.rotated = rotate(self.rotated)
    
    def to_grid(self, offset_x, offset_y):
        res = np.zeros((cache.a, cache.a))
        res[offset_y: offset_y+self.height, offset_x: offset_x+self.width] = self.rotated
        return res
    @property
    def width(self): return self.rotated.shape[1]
    @property
    def height(self): return self.rotated.shape[0]
    def __repr__(self):
        return '_'.join([''.join([
            'T' if self.pattern[y, x] else 'F' for x in range(self.pattern.shape[1])
        ]) for y in range(self.pattern.shape[0])])+str(self.rotate_time)
    @classmethod
    def all(cls):
        res = []
        print('shapes:', list_shapes)
        for _s in list_shapes:
            for rt in range(1 if cls.rotate_the_same(_s) else 4):
                res.append(cls(_s, rt))
        return res
shape_poss_type = tuple[shape, pos2]
class grid:
    def __init__(self, part:list):
        self.l = [[(1 if square(pos2(x, y)) in part else 0) for x in range(cache.a)] for y in range(cache.a)]
        self.l:ndarray = np.array(self.l, int)
    @classmethod
    def by_l(cls, l): res = super().__new__(cls); res.l = l; return res
    def __sub__(self, oth:ndarray): return self.l - oth
    def not_include(self, what, target): return what[what == target].shape == (0,)
    # -> tuple[
    #        list[list[tuple[shape, pos2, Self]]], // the argument shape, where we try to put it, the grid after sub
    #        list[tuple[shape, pos2]]              // the argument shape, where we try to put it
    #    ]
    def match(self, s: shape):
        res = []
        rposs = []
        for y in range(cache.a + 1 - s.height):
            for x in range(cache.a + 1 - s.width):
                se = self - s.to_grid(x, y) # sub_end_grid
                if se[se == -1].shape == (0,): # if shape in self
                    res.append([(s, pos2(x, y), grid.by_l(se))])
                    rposs.append((s, pos2(x, y)))

        return (res, rposs)
    # s: shape_poss_type
    # -> tuple[
    #        list[list[tuple[shape, pos2, Self]]], 
    #        list[tuple[shape, pos2]]
    #    ]
    def match_prefix(self, s, prefix:list): 
        res = []
        rposs = []
        se = self - (s[0].to_grid(s[1].x, s[1].y))
        if se[se == -1].shape == (0,): 
            res.append(prefix + [(s[0], s[1], grid.by_l(se))])
            rposs.append((s[0], s[1]))
        return (res, rposs)
    def one_num(self): return self.l.sum()
    def __repr__(self): return '_'.join([''.join(['T' if self.l[y, x] == 1 else 'F' for x in range(cache.a)]) for y in range(cache.a)])

# match_item_type = tuple[shape, pos2, grid]
# match_end_type  = list [match_item_type]
# shape_poss_type = tuple[shape, pos2]
# (match end: have the same shape, poss, len(match_end))
# state_item_type = tuple[list[match_item_type], list[shape_poss_type], int]
# get a state-like object to be added into state
def _remove(l:list, item) -> list: l.remove(item); return l
def _match(g:grid, 
           poss:list[shape_poss_type], 
           prefix:list = [],
           length:int  = 0
    ): # ->list[state_item_type]: 
    res = [] # list[state_item_type]
    # foreach possibilities in order to match by
    for s in poss:
        me, rposs = g.match_prefix(s, prefix=prefix)
        # rposs: all possibilities for matching g
        if me == []: continue
        res += [(mee, _remove(rposs, s), length) for mee in me if rposs != [s]] # delete matched
    global_rand.shuffle(res)
    return res
def match(g:grid): # -> list[match_item_type]:
    # [
    #  (what list we're foreach-ing: [MET, ...], 
    #   what shape may be matched,
    #   length)]
    state = [] # list[state_item_type]
    poss  = [] # list[shape_poss_type]
    maximum = []
    maximum_len = 0
    # init poss
    mel = [] # list[match_item_type]
    for s in shape.all():
        # me: only one shape
        me, sposs = g.match(s)
        poss += sposs
        mel += me
    if mel == []: return []
    # length equals to 1
    maximum = global_rand.choice(mel)
    maximum_len = 1
    for e in mel:
        tmp = copy(poss); tmp.remove((e[-1][0], e[-1][1]))
        if tmp == []: continue
        state.append((e, tmp, 1))
    if state == []: return []
    
    while True:
        state_now = state[-1]
        state.pop()
        poss = state_now[1]       # what the grid may include
        assert poss != []
        now = state_now[0][0][2] # what to match
        res = _match(now, poss, prefix=state_now[0], length=state_now[2]+1)
        if res == []: # match nothing
            if state == []:
                if type(maximum) != list or (maximum != [] and type(maximum[0]) != tuple):
                    assert False
                return maximum
            continue
        else:
            if res[-1][2] >= config["shape_length_minimum"]:
                return res[-1][0]
            if res[-1][2] > maximum_len:
                maximum_len = res[-1][2]
                maximum = res[-1][0]
            state += res
# class shapes(basic.poss_cls_sq): # to random
class shapes: 
    name1 = 'shape_unrotatable'
    name2 = 'shape_rotatable'
    cache = {}
    def __init__(self, name, val: once):
        self.name = name
        self.val = val
        self.collapsed = False
    @property
    def available(self):
        return (not self.collapsed) and self.val.available
    @classmethod
    def update_poss(cls, rand, all_sq: list, parts, possibilities: dict):
        global global_rand
        global_rand = rand
        for p in parts:
            g = grid(p)
            sub_pro = match(g) # list[match_item_type]
            if sub_pro != []:
                tmp = []
                for i in sub_pro:
                    _once = once(i[:2])
                    # tmp.append((cls.name1, _once))
                    tmp.append(cls(cls.name1, _once))
                    tmp.append(cls(cls.name2, _once))
                for squ in p: possibilities[squ.pos] += tmp
    def collapse(self, rand):
        self.collapsed = True
        self.val.use()
        if self.name == shapes.name1: # SU
            # return _shapes('shape_unrotatable', self.val)
            self.val = self.val.obj[0]
            return self
        else: # name2: SR
            # return _shapes('shape_rotatable', shape(self.val.obj[0].pattern, rand.randint(0, 3))) # TODO get poss from config
            self.val = shape(self.val.obj[0].pattern, rand.randint(0, 3))
            return self
    def draw(self, s, unit, surface):
        if self.name == shapes.name1: self.SU_draw(s, unit, surface)
        elif self.name == shapes.name2: self.SR_draw(s, unit, surface)
        else: assert False
    def SR_draw(self, s, unit, surface): # s: square
        row, col = self.val.rotated.shape
        d = config.IIDS * unit
        u = unit / config.SSN
        # ISRA => b, pi/2-ISRA => a, 90=>c=u
        # b/c = sin(ISRA)
        # b = c sin(ISRA) = u sin(ISRA)
        # a/c = cos(ISRA)
        # a = c cos(ISRA) = u cos(ISRA)
        b = (u-d) * config.ISRA_sin
        a = (u-d) * config.ISRA_cos
        w = row * u - d
        h = col * u - d
        t = (unit - h) / 2
        l = (unit - w) / 2
        O = p2vp(s.pos)
        for y in range(col):
            for x in range(row):
                if self.val.rotated[x, y]:
                    P1 = view_pos(O.x+l+x*u, O.y+t+y*u)
                    P2 = P1 + view_pos(b, a)
                    P3 = P2 + view_pos(a, -b)
                    P4 = P1 + view_pos(a, -b)
                    gfxdraw.aapolygon(surface, (P1, P2, P3, P4), config.ISRC)
                    gfxdraw.filled_polygon(surface, (P1, P2, P3, P4), config.ISRC)
    def SU_draw(self, s, unit, surface): # s: square
        row, col = self.val.rotated.shape
        d = config.IIDS * unit
        u = unit / config.SSN
        w = row * u - d
        h = col * u - d
        t = (unit - h) / 2
        l = (unit - w) / 2
        O = p2vp(s.pos)
        for y in range(col):
            for x in range(row):
                if self.val.rotated[x, y]:
                    draw.rect(surface, config.ISUC, 
                            (O.x+l+x*u, 
                            O.y+t+y*u, 
                            u-d, 
                            u-d))
    def __repr__(self): return f'{self.name}|{self.val}'
    def check(self, parts, sq):
        cse.log(f'cache: {shapes.cache}')
        if self.name == shapes.name1: return self.SU_check(parts, sq)
        elif self.name == shapes.name2: return self.SR_check(parts, sq)
        else: assert False
    def SU_check(self, parts, sq):
        for i, _part in enumerate(parts):
            if sq in _part:
                part_index = i
                break
        if not part_index in shapes.cache:
            g = grid(parts[part_index])
            poss = g.match(self.val)[0]
            if poss[0] == []: return False
            shapes.cache[part_index] = [[self.val, [e[0][2] for e in poss if e != []]]] # [[shape, [the grid after putting the shape]]]
        else:
            possible_g = shapes.cache[part_index][-1]
            gs = [] # to add into list
            for g in possible_g:
                poss = g.match(self.val)[0]
                gs += [e[0][2] for e in poss if e != []]
            if gs == []: return False
            shapes.cache[part_index].append([self.val, gs])
        return True
    def SR_check(self, parts, sq):
        for i, _part in enumerate(parts):
            if sq in _part:
                part_index = i
                break
        if not part_index in shapes.cache:
            shapes.cache[part_index] = []
            g = grid(parts[part_index])
            for r in range(0, 3):
                _s = shape(self.val.pattern, r)
                poss = g.match(_s)[0]
                shapes.cache[part_index] += [e[0][2] for e in poss if e != []] # [the grid after putting the shape]
            if shapes.cache[part_index] == []:
                return False
        else:
            possible_g = shapes.cache[part_index]
            gs = [] # to be tried with next
            for g in possible_g:
                for r in range(0, 3):
                    _s = shape(self.val.pattern, r)
                    poss = g.match(_s)[0]
                    gs += [e[0][2] for e in poss if e != []]
            if gs == []: return False
            shapes.cache[part_index] = gs
        return True
    @classmethod
    def prepare_to_check(cls): cls.cache = {}
    # TODO else funciton raise error