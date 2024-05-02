from json import dump, load, JSONDecodeError
from datetime import datetime
import sys

def raise_error(error:str):
    assert False
    with open('./log.txt', 'a') as f:
        f.write('[' + str(datetime.now())+ ']' + error)
    sys.exit()

def get_config():
    try:
        with open('./config.json') as f:
            config = load(f)
        return config
    except FileNotFoundError as e:
        raise_error('File config.json not found: ' + e)
    except JSONDecodeError as e:
        raise_error('Error while decoding json file: ' + e)
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
    with open('./config.json', 'w') as f:
        dump(save_, f)
def set_key_val(key:str, value):
    save_ = get_save()
    save_[key] = value
    save(save_)