from json import dump, load, JSONDecodeError
from datetime import datetime
import sys
from types import FrameType
from inspect import currentframe
from multiprocessing import current_process
import os
import shutil
from itertools import repeat, takewhile
workdir = os.path.abspath('.')
def repr_frame(f: FrameType):
    tmp = f.f_code.co_filename.replace(workdir, '.', 1)
    return f'file: {tmp}, line {f.f_lineno}, in {f.f_code.co_name}'
def repr_stack(s: list[FrameType]):
    return '\n    '.join([repr_frame(f) for f in s])
def get_stack_slice():
    frame = currentframe()
    res = [frame]
    while (frame := frame.f_back):
        if not workdir in frame.f_code.co_filename:
            break
        res.append(frame)
    return res[2:]
def call_process(): return current_process().name
def raise_error(error: str):
    assert False
    with open('./log.txt', 'a') as f:
        f.write('[' + str(datetime.now())+ ']Error: ' + error + '\n')
        f.write('    '+repr_stack(get_stack_slice())+'\nexit\n')
    shutil.move('./log.txt', './log/log_'+str(datetime.now()).replace(':', '-').replace('.', '-')+'.txt')
    with open('./log.txt', 'w'): pass
    sys.exit()
def log(s: str):
    with open('./log.txt', 'a') as f:
        f.write('[' + str(datetime.now())+ '][process: ' + call_process() +\
                ']Message: ' + s + '\n')
        # f.write('    '+repr_stack(get_stack_slice())+'\n')

def get_config():
    try:
        with open('./config.json') as f:
            config = load(f)
        return config
    except FileNotFoundError as e:
        raise_error('File config.json not found: ' + e)
    except JSONDecodeError as e:
        raise_error('Error while decoding json file: ' + e)
def get_config_by_key(key):
    try:
        with open('./config.json') as f:
            config = load(f)
        return config[key]
    except FileNotFoundError as e:
        raise_error('File config.json not found: ' + e)
    except JSONDecodeError as e:
        raise_error('Error while decoding json file: ' + e)
    except KeyError as e:
        raise_error('Key not found: ' + e)
def set_config(val):
    with open('./config.json', 'w') as f:
        dump(val, f)

def get_save():
    try:
        with open('./save.json') as f:
            save_ = load(f)
        return save_
    except FileNotFoundError as e:
        raise_error('File save.json not found: ' + e)
def get_key_val(key):
    try:
        with open('./save.json') as f:
            save_ = load(f)
        return save_[key]
    except FileNotFoundError as e:
        raise_error('File save.json not found: ' + e)
    except KeyError as e:
        raise_error('Key not found while reading save: ' + e)
def save(save_):
    with open('./save.json', 'w') as f:
        dump(save_, f)
def set_key_val(key:str, value):
    save_ = get_save()
    save_[key] = value
    save(save_)
def clear(max):
    with open('./log.txt') as f:
        buff_generate = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(0)))
        line_count = sum(buff.count('\n') for buff in buff_generate)
    if line_count > max - 2:
        with open('./log.txt', 'w') as f:
            pass
clear(get_config_by_key("log_max_line_count"))