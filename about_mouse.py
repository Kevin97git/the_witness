from functools import lru_cache
from typing import Iterable

from constant_type import *
t = True
f = False
v = 'vertical'
h = 'horizonal'

class cmp_union:
    def __init__(self, vals: Iterable) -> None:
        self.values = vals
    def __eq__(self, oth) -> bool:
        return oth in self.values
    def __ne__(self, oth) -> bool:
        return not self == oth 
p2vpo = None
state = {}
view_vec = None
def set_view_vec(vv): global view_vec; view_vec = vv
@lru_cache
def near_line(point, horizonalon, positiveon):
    return ((point.right_line if positiveon else point.left_line)
            if horizonalon
            else (point.down_line if positiveon else point.up_line))
@lru_cache
def near_point(point, horizonalon, positiveon):
    return ((point.right_obj if positiveon else point.left_obj)
            if horizonalon
            else (point.down_obj if positiveon else point.up_obj))
def available(point, horizonalon, positiveon):
    target = near_line(point, horizonalon, positiveon)

    # check situation like
    '''
         |
         |
    -----P-----
    '''
    if target and target.draw_progress.progress.length == 0:
        ps = [target.p1, target.p2]
        ps.remove(point)
        P = ps[0] # get P
        l = P.near_line()
        l.remove(target) # get P near_line but not target
        l = [e for e in l if e and e.draw_progress.progress.length != 0] # get -----
    else: l = []
    print('available' if (
        not target is None 
        and target.type != 'line_cannot_pass'
    ) else 'unavailable', (
        'simple' if l == []
        else 'special'), target)
    return (
        not target is None 
        and target.type != 'line_cannot_pass'
        and l == []
    )
def drawed_and_not_from_here(point, horizonalon, positiveon):
    target = near_line(point, horizonalon, positiveon)
    # print('danfh' if (target.draw_progress != view_vec(0, 0) and (target.draw_progress.positive != positiveon)) else 'ndanfh', target)
    print('danfh' if target.draw_progress.progress != view_vec(0, 0) and (target.draw_progress.dcsp != point) else 'ndanfh', target)
    return target.draw_progress.progress != view_vec(0, 0) and (target.draw_progress.dcsp != point)
danfh = drawed_and_not_from_here
class draw_progress:
    def __init__(self, dcsp, prg):
        self.dcsp = dcsp
        self.progress = prg
    @classmethod
    def null(cls):
        return draw_progress(None, view_vec(0, 0))
    def __repr__(self) -> str:
        return 'dprog_frm'+repr(self.dcsp)+'val'+repr(self.progress)
    def __eq__(self, oth: object) -> bool:
        try: return self.dcsp == oth.dcsp and self.progress == oth.progress
        except: 
            try: return self.progress == oth.progress
            except: return False
    def to_linese(self, draw_ps, area):
        '(draw_simply_start, area) => line_draw_p1, line_draw_p2'
        if self.progress.positive:
            return (draw_ps, draw_ps + self.progress)# TODO I'm not sure
        else:
            return (draw_ps + area + self.progress, draw_ps + area)
def set_p2vpo(_p2vpo): global p2vpo; p2vpo = _p2vpo
def set_dcsp(p_start): global state; state['dcsp'] = p_start; state['now_line'] = p_start.right_line; state['allowed_poson'] = cmp_union([True, False])
def get_nl(): return state['now_line']
def set_state(turning, danfh, horizonalon, positiveon):
    print('set_state', turning, danfh, horizonalon, positiveon)
    state['direction'] = h if horizonalon else v
    if danfh: state['dcsp'] = near_point(turning, horizonalon, positiveon)
    else: state['dcsp'] = turning
    state['now_line'] = near_line(turning, horizonalon, positiveon)
    state['allowed_poson'] = not positiveon if danfh else positiveon
    print('set_state_end', state)
def rectify(nmp):
    '''
    input: now mouse position(nmp)
    output: mouse move after rectifying
    please use this result to call d2prog with
    '''
    dcspos = p2vpo(state['dcsp'].pos)
    print('rectify', dcspos, state['dcsp'])
    if state['direction'] == 'horizonal': nmp.y = dcspos.y
    elif state['direction'] == 'vertical': nmp.x = dcspos.x
    else:
        print('unavailable')
        nmp.x = dcspos.x; nmp.y = dcspos.y
    d = nmp - dcspos
    if d.positive != state['allowed_poson']:
        print('nallow positiveon(d, a)', d.positive, state['allowed_poson'])
        nmp.x = dcspos.x; nmp.y = dcspos.y
    _max = dcspos + (state['now_line'].area if state['allowed_poson'] else -(state['now_line'].area))
    if ((nmp > _max) if state['allowed_poson'] else (nmp < _max)): nmp.x = _max.x; nmp.y = _max.y
    print('rectify_res', nmp - dcspos)
    return nmp - dcspos
vv_horizonal = lambda d: -MMDA < d.slope < MMDA
vv_vertical = lambda d: -1/MMDA > d.slope or d.slope > 1/MMDA
def fill_an(turning, horizonalon, positiveon, unit):
    print('fillan', horizonalon, positiveon)
    l = turning.near_line()
    l.remove(near_line(turning, horizonalon, positiveon))
    # l = [e for e in l if e and abs(e.draw_progress.length) >= e.area.length - MCR * unit - OAMMM * unit]
    for e in l:
        if e is None: continue
        if e.draw_progress.dcsp == turning: e.clear()
        if e.draw_progress.progress.length >= e.area.length - MCR * unit - OAMMM * unit:
            if e.draw_progress.progress == e.area: continue
            print('fill(l, prog, area, proglen, dcslen)', e, e.draw_progress.progress, e.area, e.draw_progress.progress.length, e.area.length - MCR * unit - OAMMM * unit)
            e.fill()
            # print('aft fill', e.draw_progress.progress)
        elif e.draw_progress.progress.length != 0:
            print('clear(l, prog, area, proglen, dcslen)', e, e.draw_progress.progress, e.area, e.draw_progress.progress.length, e.area.length - MCR * unit - OAMMM * unit)
            e.clear()
    print('fillane')
def at_turning(turning, nmp, unit):
    '''
    check collide first
    turning: point
    available: (point, horizonalon, positiveon) -> bool
    fill: (point, horizonalon, positiveon) -> None
    set_now_line: (point, horizonalon, positiveon) -> None
    '''
    global state
    tpos = p2vpo(turning.pos)
    d = nmp - tpos
    print('call_at_turning', turning, 'dslope', d.slope, end=':')
    print('h' if vv_horizonal(d) else ('v' if vv_vertical(d) else 'p'), d.positive)
    if vv_horizonal(d):
        d.y = 0
        d.x = d.x if d.x < OAMMM * unit else OAMMM * unit
        if available(turning, True, d.positive):
            _danfh = danfh(turning, True, d.positive)
            set_state(turning, _danfh, t, d.positive)
            # TODO TRY
            # if not _danfh: fill_an(turning, True, d.positive, unit)
            fill_an(turning, True, d.positive, unit)
    elif vv_vertical(d):
        d.x = 0
        d.y = d.y if d.y < OAMMM * unit else OAMMM * unit
        if available(turning, False, d.positive):
            _danfh = danfh(turning, False, d.positive)
            set_state(turning, _danfh, f, d.positive)
            # TODO TRY
            # if not _danfh: fill_an(turning, False, d.positive, unit)
            fill_an(turning, False, d.positive, unit)
    state['direction'] = state['direction'] if 'direction' in state else 'unavailable'
    # print('state', state)
def d2progress(d): return draw_progress(state['dcsp'], d) # well, I'm serious
