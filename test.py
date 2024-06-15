from collections import namedtuple
from typing import Any
class vv(namedtuple('vvs', 'x y')):
    def __new__(cls, x, y):   return super().__new__(cls, x, y)
    def __setattr__(self, name: str, value: Any) -> None:
        return object.__setattr__(self, name, value)
a = vv(1, 2)
a.x = 0