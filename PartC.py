from pymonad import Maybe
from pymonad.Maybe import Just, Nothing
from math import sqrt
from functools import partial
from typing import Callable, Any

# define safe sqrt, returns Nothing if the val is less than zero, else returns the Just wrapped sqrt result
def safeSqrt(val: float) -> Maybe:
    return Nothing if val < 0 else Just(sqrt(val))

# Infix class for defining our own operator
class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

# define our custom operator that is a combo of function composition and bind
@Infix
def bpos(f1: Callable[[Any], Maybe], f2: Callable[[Any], Maybe]) -> Callable[[Any], Maybe]:
    return lambda x: f1(x) >> f2

# define our safe root function which uses the safeSqrt with the custom operator I created
def safeRoot(val: int) -> Callable[[float], Maybe]:
    return Just if val <= 0 else safeSqrt |bpos| safeRoot(val - 1)

# define our 1st test case for safeRoot
def testSafeRoot(n: int) -> Maybe:
    return safeRoot(n)(2**(2**n))

# define a boolean test on testing values up to 10 players
def testSafeRootTo9() -> bool:
    return all(testSafeRoot(n) == Just(2) for n in range(10))

# define the operation to perform when the script is launched as main
if __name__ == "__main__":
    x = testSafeRootTo9()
    print(x)