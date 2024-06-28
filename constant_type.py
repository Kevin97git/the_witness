from typing import Any, Literal, List
import math
from pygame import locals

import config_save_error as cse
config = cse.get_config()


puzzle_module_load_func = cse.basic.puzzle_module_load_func
puzzle_module_load_cls  = cse.basic.puzzle_module_load_cls
cse.basic.set_cse(cse)

try:
    # TIP #= at the end of a line means this turn to basic.py
    # A_MAX = config["a_max"] #=
    # A_MIN = config["a_min"] #=
    PGT   = config["puzzle_generate_timeout"]
    TICK  = config["tick_rate"]
    PSPI   = config["puzzle_square_proportion_min"]
    PSPA   = config["puzzle_square_proportion_max"]
    PLPI  = config["puzzle_line_proportion_min"]
    PLPA  = config["puzzle_line_proportion_max"]



    wwidth = config["width"]
    wheight = config["height"]
    tb_border = config["top_bottom_border"]
    LINE_WIDTH = config["line_width"]
    lr_border = int((wwidth - (wheight - tb_border*2)) / 2)
    line_color = config["line_color"]
    special_point_length = config["start|end_point_length"]
    BGC = config["back_ground_color"]
    RBR = config["rect_border_radius"]
    MCR = config["mouse_collide_radius"]
    MMDA = math.tan(math.radians(config["mouse_movement_deciding_angle"]))
    OAMMM = config["once_available_max_mouse_move"]

    key_bound_dict: dict[str, str] = config["key_bound"]
    for k in key_bound_dict:
        try:
            key_bound_dict[k] = eval(f'locals.K_{key_bound_dict[k].upper()}')
        except AttributeError:
            key_bound_dict[k] = eval(f'locals.K_{key_bound_dict[k].lower()}')
    class keybound_cls:
        def __init__(self):
            self.__dict__ = key_bound_dict
    key_bound = keybound_cls()
except KeyError as k:
    cse.raise_error(f'key {k} not found when reading config.json')
except Exception as e:
    cse.raise_error(f'error when reading config: {e}')