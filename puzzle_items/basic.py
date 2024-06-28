'''
each module in dir puzzle_items should import this, just
>>> from . import basic
maybe then
>>> from .basic import xxx

before this moudle is loaded, func set_raise_error must be called in the moudule "config_save_error.py"
so import config_save_error first in main, then it'll call this, then main will load modules in puzzle_items
'''
from json import load, JSONDecodeError
from typing import Any
import math

class once:
    def __init__(self, obj):
        self.obj = obj
        self.available = True
    def use(self): self.available = False
    def __repr__(self): return 'once'+repr(self.obj)
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
    class config_cls:
        def __init__(self):
            self.A_MAX = _config["a_max"]
            self.A_MIN = _config["a_min"]
            self.PI_color = _config["part_mark_color"]
            self.LPN_color = _config["icon_triangle_color"]
            self.SIS = _config["single_icon_size"]
            self.RBR = _config["rect_border_radius"]
            self.SSN = _config["square_split_number"]
            self.IIDLPN = _config["icon_item_distance"]["triangle"]
            self.IIDS = _config["icon_item_distance"]["shapes"]
            self.GL1 = ((self.SSN-1)/2)/self.SSN # LPN draw guide line 1
            self.GL2 = ((self.SSN+1)/2)/self.SSN # LPN draw guide line 2
            self.ISRC = _config["icon_shape_rotatable_color"]
            self.ISUC = _config["icon_shape_unrotatable_color"]
            self.ISRA = math.radians(_config["icon_shape_rotatable_angle"])
            self.ISRA_sin = math.sin(self.ISRA)
            self.ISRA_cos = math.cos(self.ISRA)
            self.LINE_WIDTH = _config["line_width"]
            self.shapes = _config["shapes"]
            self.line_color = _config["line_color"]
        def __getitem__(self, ind):
            return _config[ind]
    config = config_cls()
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
    except Exception as e:      raise_error(f'error when reading file {filename}: {e}')
    return cls

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
