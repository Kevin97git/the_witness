from typing import Any, Literal, List
import math

import config_save_error as cse
config = cse.get_config()

A_MAX = config["a_max"]
A_MIN = config["a_min"]
CMDRM = config["cmd_read_max"]
PGT   = config["puzzle_generate_timeout"]
TICK  = config["tick_rate"]
SMM   = config["seed_mix_method"]
PSP   = config["puzzle_square_proportion"]
PLPI  = config["puzzle_line_proportion_min"]
PLPA  = config["puzzle_line_proportion_max"]
match SMM:
    case 'XOR':
        SMM = lambda x, y: x^y
    case _:
        SMM = lambda x, y: x^y



wwidth = config["width"]
wheight = config["height"]
tb_border = config["top_bottom_border"]
LINE_WIDTH = config["line_width"]
lr_border = int((wwidth - (wheight - tb_border*2)) / 2)
line_color = config["line_color"]
special_point_length = config["start|end_point_length"]
shape_length_minimum = config["shape_length_minimum"]
config_shapes: List[str] = config["shapes"]
PI_color = config["part_mark_color"]
LPN_color = config["icon_triangle_color"]
BGC = config["back_ground_color"]
SIS = config["single_icon_size"]
RBR = config["rect_border_radius"]
SSN = config["square_split_number"]
IIDLPN = config["icon_item_distance"]["triangle"]
IIDS = config["icon_item_distance"]["shapes"]
GL1 = ((SSN-1)/2)/SSN # LPN draw guide line 1
GL2 = ((SSN+1)/2)/SSN # LPN draw guide line 2
ISRC = config["icon_shape_rotatable_color"]
ISUC = config["icon_shape_unrotatable_color"]
ISRA = math.radians(config["icon_shape_rotatable_angle"])
ISRA_sin = math.sin(ISRA)
ISRA_cos = math.cos(ISRA)
MCR = config["mouse_collide_radius"]
MMDA = math.tan(math.radians(config["mouse_movement_deciding_angle"]))
OAMMM = config["once_available_max_mouse_move"]


# probabilities include const
LPN = 'line_passed_number: '
PI  = 'part_index: '
SU  = 'shape_unrotatable: '
SR  = 'shape_rotatabele: '
LMP = 'line_must_pass'
LCP = 'line_cannot_pass'



