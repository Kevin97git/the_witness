from . import basic
from .basic import square, view_pos, config, p2vp, draw_triangle
class LPN(basic.poss_cls_sq):
    name = 'num_of_line_pass_by'
    def __init__(self, val):
        self.val = val
    @classmethod
    def update_poss(cls, rand, all_sq: list, parts, possibilities: dict):
        for s in all_sq:
            t = s.line_passed
            if t != 0:
                possibilities[s.pos].append(cls(t))
    @property
    def available(self):
        return True
    def collapse(self, rand):
        return self
    def draw(self, s, unit, surface):
        GL1 = config.GL1
        GL2 = config.GL2
        SSN = config.SSN
        LPN_color = config.LPN_color
        IIDLPN = config.IIDLPN
        O = p2vp(s.pos)
        scaler = 1
        u = unit / SSN * scaler
        d = IIDLPN * unit * scaler
        uad = view_pos(u + d, 0)
        match self.val:
            case 1:
                A1 = O + view_pos(0.5 * u * SSN, GL1 * u * SSN)
                B1 = O + view_pos(GL1 * u * SSN, GL2 * u * SSN)
                C1 = O + view_pos(GL2 * u * SSN, GL2 * u * SSN)
                draw_triangle(surface, A1, B1, C1, LPN_color)
            case 2:
                A1 = O + view_pos(2 * u - d / 2, GL1 * u * SSN)
                B1 = O + view_pos(1.5 * u - d / 2, GL2 * u * SSN)
                C1 = O + view_pos(2.5 * u - d / 2, GL2 * u * SSN)
                draw_triangle(surface, A1, B1, C1, LPN_color)
                A2 = A1 + uad
                B2 = B1 + uad
                C2 = C1 + uad
                draw_triangle(surface, A2, B2, C2, LPN_color)
            case 3:
                A1 = O + view_pos(0.5 * u * SSN, 1.5 * u - d / 2)
                B1 = O + view_pos(GL1 * u * SSN, 2.5 * u - d / 2)
                C1 = O + view_pos(GL2 * u * SSN, 2.5 * u - d / 2)
                draw_triangle(surface, A1, B1, C1, LPN_color)
                A2 = O + view_pos(2 * u - d / 2, GL1 * u * SSN + u / 2 + d / 2)
                B2 = O + view_pos(1.5 * u - d / 2, GL1 * u * SSN + 1.5 * u + d / 2)
                C2 = O + view_pos(2.5 * u - d / 2, GL1 * u * SSN + 1.5 * u + d / 2)
                draw_triangle(surface, A2, B2, C2, LPN_color)
                A3 = A2 + uad
                B3 = B2 + uad
                C3 = C2 + uad
                draw_triangle(surface, A3, B3, C3, LPN_color)
            case 4: assert False
    def __repr__(self) -> str:
        return f'{LPN.name}|{self.val}'
    def check(self, parts, sq) -> bool:
        return sq.line_passed == self.val
    @classmethod
    def prepare_to_check(self): pass
    