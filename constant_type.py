from typing import Any, Literal, List
import math

import config_save_error as cse
config = cse.get_config()


# puzzle_config = cse.basic.puzzle_config
# test_arg = cse.basic.test_arg
# test_res = cse.basic.test_res
puzzle_module_load_func = cse.basic.puzzle_module_load_func
puzzle_module_load_cls  = cse.basic.puzzle_module_load_cls
cse.basic.set_cse(cse)


# A_MAX = config["a_max"]
# A_MIN = config["a_min"]
CMDRM = config["cmd_read_max"]
PGT   = config["puzzle_generate_timeout"]
TICK  = config["tick_rate"]
SMM   = config["seed_mix_method"]
PSPI   = config["puzzle_square_proportion_min"]
PSPA   = config["puzzle_square_proportion_max"]
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
BGC = config["back_ground_color"]
RBR = config["rect_border_radius"]
MCR = config["mouse_collide_radius"]
MMDA = math.tan(math.radians(config["mouse_movement_deciding_angle"]))
OAMMM = config["once_available_max_mouse_move"]


# possibilities include const

# LPN = 'line_passed_number: '
# PI  = 'part_index: '
# SU  = 'shape_unrotatable: '
# SR  = 'shape_rotatabele: '
# LMP = 'line_must_pass'
# LCP = 'line_cannot_pass'



