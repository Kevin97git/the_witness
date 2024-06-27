from . import basic
from .basic import poss_cls_l, config
class line_cannot_pass(poss_cls_l):
    name = 'line_cannot_pass'
    def __init__(self) -> None:
        self.name = line_cannot_pass.name
        self.color = config.line_color[self.name]
        self.passable = False
    @classmethod
    def update_poss(cls, rand, alll: list, possibilities: dict):
        el = [l for l in alll if not l.exist]
        for l in el: possibilities[l.id].append(cls())
    @property
    def available(self): return True
    def collapse(self, rand): return self
    def __repr__(self): return f'{self.name}'
    @property
    def is_simple(self): return False
    def check(self, l) -> bool: assert not l.is_on(); return not l.is_on()