from . import basic
from .basic import square, config, p2vpo, draw_radius_border_rect
class PI(basic.poss_cls_sq):
    # PI_color = config["part_mark_color"]
    PI_color = config.PI_color
    name = 'part_index'
    cache = {} # key: val; val: npi
    def __init__(self, val):
        self.val = val
    @classmethod
    def update_poss(cls, rand, all_sq: list, parts, possibilities: dict):
        # print(list(range(len(parts))), len(cls.PI_color))
        able_ind = rand.sample(list(range(len(parts))), min(len(parts), len(cls.PI_color)))
        for ind, p in enumerate(parts):
            for e in p:
                if ind in able_ind:
                    possibilities[e.pos].append(cls(able_ind.index(ind)))
    @property
    def available(self):
        return True
    def collapse(self, rand):
        return self
    def draw(self, s, unit, surface):
        draw_radius_border_rect(config.PI_color[self.val], 
            p2vpo(s.pos, ((1-config.SIS)*unit/2+config.LINE_WIDTH, (1-config.SIS)*unit/2+config.LINE_WIDTH)), 
            config.SIS*unit, config.SIS*unit, surface)
    def __repr__(self):
        return f'{self.name}|{self.val}'
    def check(self, parts, sq) -> bool: 
        for i, _part in enumerate(parts):
            if sq in _part:
                now_part_index = i
                break
        basic.cse.log(f'pi check: {PI.cache}, checking_part_ind={now_part_index}')
        if self.val in PI.cache:
            if now_part_index != PI.cache[self.val]:
                return False
        else:
            PI.cache[self.val] = now_part_index
        return True
    @classmethod
    def prepare_to_check(cls):
        cls.cache = {}