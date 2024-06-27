'''
each module in dir puzzle_items should import this, just
>>> from . import basic
maybe then
>>> from .basic import xxx
function in these module should return test_res when arg is test_arg, it should have only one argument
or use decorator p_init_f

before this moudle is loaded, func set_raise_error must be called in the moudule "config_save_error.py"
so import config_save_error first in main, then it'll call this, then main will load modules in puzzle_items
'''
from json import load, JSONDecodeError
from typing import Any
import math

# TODO delete debug
next_id = 0
def get_id(): global next_id; return (next_id := next_id+1)
class once:
    def __init__(self, obj):
        self.obj = obj
        self.available = True
        self.id = get_id()
    def use(self): self.available = False
    def __repr__(self): return str(self.id)+repr(self.obj)
class poss_cls_sq:
    def __init__(self) -> None: pass
    @classmethod
    def update_poss(cls, rand, all_sq: list, parts, possibilities: dict): pass
    @property
    def available(self): return False
    def collapse(self, rand): return None
    def draw(self, s, unit, surface): pass
    def check(self, parts, sq) -> bool: return False
    @classmethod
    def prepare_to_check(self): pass
class poss_cls_l:
    def __init__(self) -> None: pass
    @classmethod
    def update_poss(cls, rand, all_l: list, possibilities: dict): pass
    @property
    def available(self): return False
    def collapse(self, rand): return None
    def draw(self, s, unit, surface): pass
    @property
    def is_simple(self): return False
    def check(self, l) -> bool: return False
def set_config(__config):
    global _config, config
    _config = __config
    class config:
        A_MAX = _config["a_max"]
        A_MIN = _config["a_min"]
        PI_color = _config["part_mark_color"]
        LPN_color = _config["icon_triangle_color"]
        SIS = _config["single_icon_size"]
        RBR = _config["rect_border_radius"]
        SSN = _config["square_split_number"]
        IIDLPN = _config["icon_item_distance"]["triangle"]
        IIDS = _config["icon_item_distance"]["shapes"]
        GL1 = ((SSN-1)/2)/SSN # LPN draw guide line 1
        GL2 = ((SSN+1)/2)/SSN # LPN draw guide line 2
        ISRC = _config["icon_shape_rotatable_color"]
        ISUC = _config["icon_shape_unrotatable_color"]
        ISRA = math.radians(_config["icon_shape_rotatable_angle"])
        ISRA_sin = math.sin(ISRA)
        ISRA_cos = math.cos(ISRA)
        LINE_WIDTH = _config["line_width"]
        shapes = _config["shapes"]
        line_color = _config["line_color"]
def set_raise_error(_raise_err):
    global raise_error
    raise_error = _raise_err
def get_puzzle():
    try:
        with open('./puzzle_items/puzzle_config.json') as f:
            puzzle = load(f)
        return puzzle
    except FileNotFoundError as e:
        raise_error('File config.json not found: ' + e)
    except JSONDecodeError as e:
        raise_error('Error while decoding json file: ' + e)
def set_cse(_cse): global cse; cse = _cse

puzzle_config = get_puzzle()

if not "test_arg" in puzzle_config:
    raise_error('Key not found in puzzle.json: "test_arg"')
test_arg = puzzle_config["test_arg"]
if not "test_res" in puzzle_config:
    raise_error('Key not found in puzzle.json: "test_res"')
test_res = puzzle_config["test_res"]
if not "square_poss" in puzzle_config:
    raise_error('Key not found in puzzle.json: "square_poss"')
square_poss = puzzle_config["square_poss"]
if not "line_poss" in puzzle_config:
    raise_error('Key not found in puzzle.json: "line_poss"')
line_poss = puzzle_config["line_poss"]


def puzzle_module_load_func(key):
    if not key in puzzle_config:
        raise_error('Key not found in puzzle_config.json: '+repr(key))
    if (type(puzzle_config[key]) != list 
        or len(puzzle_config[key]) != 2 
        or type(puzzle_config[key][0]) != str 
        or type(puzzle_config[key][1]) != str):
        raise_error('puzzle_config.json item type error: should be like [str, str] but'+repr(puzzle_config[key]))
    filename, funcname = puzzle_config[key]
    try:
        exec(f'from . import {filename} as puzzle_items_{filename}')
        f = eval(f'puzzle_items_{filename}.{funcname}')
    except ModuleNotFoundError: raise_error(f'there\'s no module {filename}')
    except AttributeError:      raise_error(f'there\'s no {funcname} in the module {filename}')
    except Exception as e:      raise_error(f'error when reading file {filename}: {e}')
    try: 
        assert f(test_arg) == test_res
    except Exception as e:      raise_error(f'error when calling file {filename}: {e}')
    return f
def puzzle_module_load_cls(key) -> poss_cls_sq|poss_cls_l:
    if not key in puzzle_config:
        raise_error('Key not found in puzzle_config.json: '+repr(key))
    if (type(puzzle_config[key]) != list 
        or len(puzzle_config[key]) != 2 
        or type(puzzle_config[key][0]) != str 
        or type(puzzle_config[key][1]) != str):
        raise_error('puzzle_config.json item type error: should be like [str, str] but'+repr(puzzle_config[key]))
    filename, clsname = puzzle_config[key]
    try:
        exec(f'from . import {filename} as puzzle_items_{filename}')
        cls = eval(f'puzzle_items_{filename}.{clsname}')
    except ModuleNotFoundError: raise_error(f'there\'s no module {filename}')
    except AttributeError:      raise_error(f'there\'s no {clsname} in the module {filename}')
    # TODO delete # in the following line
    # except Exception as e:      raise_error(f'error when reading file {filename}: {e}')
    return cls

def p_init_f(function):
    a = test_arg
    r = test_res
    def f(rand):
        if rand == a: return r
        return function(rand)
    return f
def set_5basic_cls(_point, _line, _square, _pos2, _view_pos):
    global point, line, square, pos2, view_pos
    point = _point; line = _line; square = _square; pos2 = _pos2; view_pos = _view_pos
def set_5basic_func(_set_a, _p2vp, _p2vpo, _draw_triangle, _draw_radius_border_rect):
    global set_a, p2vp, p2vpo, draw_radius_border_rect, draw_triangle
    set_a = _set_a; p2vp = _p2vp; p2vpo = _p2vpo; draw_radius_border_rect = _draw_radius_border_rect; draw_triangle = _draw_triangle

cache_dict = {
    'a': -1,
    'point_start': None,
    'point_end': None
}
class cache_cls:
    def __init__(self) -> None:
        pass
    def __getattr__(self, name: str) -> Any:
        return cache_dict[name]
    def __setattr__(self, name: str, value: Any) -> None:
        cache_dict[name] = value
cache = cache_cls()
