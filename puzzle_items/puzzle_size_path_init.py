from . import basic
from .basic import config, set_a, point, line, square, pos2, cache
from copy import copy
A_MIN = config.A_MIN
A_MAX = config.A_MAX
def path_sidesway(l, rand): # l: line
    def _rand_bool(a:int, b:int): return 0 in rand.sample([i for i in range(b)], a)
    while True:
        if l.horizonal: return False
        if not l.exist: return False
        #left
        if (
            (not l.left_obj is None)
            and (not l.left_obj.exist)
            and (not line(l.p1.left_obj, l.p1).exist)
            and (not l.p1.left_obj.passed)
            and (not line(l.p2.left_obj, l.p2).exist)
            and (not l.p2.left_obj.passed)
        ):
            if _rand_bool(1, 4):
                l.left_obj.on()
                l.off()
                line(l.p1.left_obj, l.p1).on()
                line(l.p2.left_obj, l.p2).on()
                continue
            else: break
        if (
            (not l.right_obj is None)
            and (not l.right_obj.exist)
            and (not line(l.p1, l.p1.right_obj).exist)
            and (not l.p1.right_obj.passed)
            and (not line(l.p2, l.p2.right_obj).exist)
            and (not l.p2.right_obj.passed)
        ):
            if _rand_bool(1, 4):
                l.right_obj.on()
                l.off()
                line(l.p1, l.p1.right_obj).on()
                line(l.p2, l.p2.right_obj).on()
                continue
            else: break
        return False
def intersection(a:list, b:list):
    return list(set(a).intersection(set(b)))
def sub(a:list, b:list):
    return list(set(a)-set(b))
def way_log_info(ps, pe):
    ons = []
    for lid in line.all():
        l = line.by_id(lid)
        if l.exist:
            ons.append(l)

    cons = copy(ons)
    p_passby = []
    np = ps
    direction = None
    while True:
        nl = intersection(np.near_line(), cons)[0]
        cons.remove(nl)
        othp = sub([nl.p1, nl.p2], [np])[0]
        if np.y == othp.y:
            if direction != 'vertical':
                direction = 'vertical'
                p_passby.append(np)
        elif np.x == othp.x:
            if direction != 'horizonal':
                direction = 'horizonal'
                p_passby.append(np)
        if othp == pe:
            p_passby.append(pe)
            break
        np = othp

    return f'{ons}\n{p_passby}'
    
def init(rand):
    # init size
    a = rand.randint(A_MIN, A_MAX)
    set_a(a)
    square.set_by_a(a)
    point_start   = point(pos2(0, rand.randint(0, a)))
    point_end     = point(pos2(a, rand.randint(0, a)))
    turning_point = [ point(pos2(i, rand.randint(0, a))).on() for i in range(a) ]
    assert not (point_start is None or point_end is None or None in turning_point)
    point_start.on()
    point_end.on()
    basic.cse.log(f'point_start&end: {point_start}, {point_end}')
    # connect them
    last = point_start
    for p in turning_point:
        if p != last: line.from_to_untidy(p, last)
        last = p.right_obj
        line(p, last).on()
    if last != point_end: line.from_to_untidy(last, point_end)
    # sidesway
    for l in copy(list(line.all().values())): path_sidesway(l, rand)
    basic.cse.log('way: '+way_log_info(point_start, point_end))
    cache.a = a
    cache.point_start = point_start
    cache.point_end   = point_end
    return a