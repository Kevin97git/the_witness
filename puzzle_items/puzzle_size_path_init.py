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

@basic.p_init_f
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
    
    # connect them
    last = point_start
    for p in turning_point:
        if p != last: line.from_to_untidy(p, last)
        last = p.right_obj
        line(p, last).on()
    if last != point_end: line.from_to_untidy(last, point_end)
    # sidesway
    for l in copy(list(line.all().values())): path_sidesway(l, rand)

    cache.a = a
    cache.point_start = point_start
    cache.point_end   = point_end
    return a