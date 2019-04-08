from typing import Callable, TypeVar
from pymonad import Maybe, Nothing
from pymonad.Maybe import Just

#define our Expr Class
class Expr:
    pass

#define our Div Class
class Div(Expr):
    def __init__(self, a: Expr, b: Expr):
        self.a = a
        self.b = b

#define our Val Class
class Val(Expr):
    def __init__(self, n: int):
        self.n = n

#define a safediv using Pymonad maybe
def safediv(a: int, b: int) -> Maybe:
    if b == 0:
        return Nothing
    else:
        return Just((a//b))

#define eval using the bind syntax presented in the video
def eval(exp: Expr) -> Maybe:
    if isinstance(exp, Val):
        return Just(exp.n)
    elif isinstance(exp, Div):
        return eval(exp.a) >> (lambda x:\
                eval(exp.b) >> (lambda y:\
                    safediv(x, y)))

#define eval, try using the do syntax used in the video
def eval_do(exp: Expr) -> Maybe:
    if isinstance(exp, Val):
        return Just(exp.n)
    elif isinstance(exp, Div):
        n = eval_do(exp.a)
        m = eval_do(exp.b)
        return safediv(n.getValue(), m.getValue()) if n and m else None

#test the functions
if __name__ == "__main__":
    x = safediv(10, 2)
    print(x)
    print(x.getValue())
    print(eval(Div(Val(6), Val(2))))
    print(eval(Div(Val(6), Val(0))))
