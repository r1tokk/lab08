from __future__ import annotations

from typing import Final

from expr import Add, Bin, Div, Expr, Expr2, Mul, Num, Num2, Sub

MAX_ABS: Final[int] = 10_000


class EvalOverflow(ValueError):
    """Виняток при перевищенні допустимого діапазону значень."""


class DivisionByZeroError(ZeroDivisionError):
    """Виняток при діленні на нуль під час обчислення AST."""


def _check_range(x: int) -> int:
    if abs(x) > MAX_ABS:
        raise EvalOverflow(f"overflow: {x}")
    return int(x)


def eval_expr(e: Expr) -> int:
    """Чисте обчислення арифметичного дерева через структурний pattern matching."""
    match e:
        case Num(v):
            return _check_range(v)
        case Add(a, b):
            return _check_range(eval_expr(a) + eval_expr(b))
        case Sub(a, b):
            return _check_range(eval_expr(a) - eval_expr(b))
        case Mul(a, b):
            return _check_range(eval_expr(a) * eval_expr(b))
        case Div(a, b):
            denom = eval_expr(b)
            if denom == 0:
                raise DivisionByZeroError("Division by zero in expression")
            return _check_range(eval_expr(a) // denom)
        case _:
            raise RuntimeError(f"Невідомий вузол: {e}")


def fold_constants(e: Expr) -> Expr:
    """Згортання констант (constant folding) та базові алгебраїчні спрощення."""
    match e:
        case Num():
            return e
        case Add(a, b):
            fa, fb = fold_constants(a), fold_constants(b)
            match (fa, fb):
                case (Num(va), Num(vb)):
                    return Num(va + vb)
                case (Num(0), right_expr):
                    return right_expr
                case (left_expr, Num(0)):
                    return left_expr
                case _:
                    return Add(fa, fb)
        case Sub(a, b):
            fa, fb = fold_constants(a), fold_constants(b)
            match (fa, fb):
                case (Num(va), Num(vb)):
                    return Num(va - vb)
                case (left_expr, Num(0)):
                    return left_expr
                case _:
                    return Sub(fa, fb)
        case Mul(a, b):
            fa, fb = fold_constants(a), fold_constants(b)
            match (fa, fb):
                case (Num(va), Num(vb)):
                    return Num(va * vb)
                case (Num(0), _) | (_, Num(0)):
                    return Num(0)
                case (Num(1), right_expr):
                    return right_expr
                case (left_expr, Num(1)):
                    return left_expr
                case _:
                    return Mul(fa, fb)
        case Div(a, b):
            fa, fb = fold_constants(a), fold_constants(b)
            match (fa, fb):
                case (_, Num(0)):
                    return Div(fa, fb)
                case (Num(va), Num(vb)):
                    return Num(va // vb)
                case (left_expr, Num(1)):
                    return left_expr
                case _:
                    return Div(fa, fb)
        case _:
            return e


def eval_expr2(e: Expr2) -> int:
    """Обчислення альтернативної форми AST із Literal-операторами."""
    match e:
        case Num2(v):
            return _check_range(v)
        case Bin("+", a, b):
            return _check_range(eval_expr2(a) + eval_expr2(b))
        case Bin("-", a, b):
            return _check_range(eval_expr2(a) - eval_expr2(b))
        case Bin("*", a, b):
            return _check_range(eval_expr2(a) * eval_expr2(b))
        case Bin("/", a, b):
            denom = eval_expr2(b)
            if denom == 0:
                raise DivisionByZeroError("Division by zero in expression")
            return _check_range(eval_expr2(a) // denom)
        case _:
            raise RuntimeError(f"Невідомий вузол або оператор: {e}")
