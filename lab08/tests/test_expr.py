from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from eval_ import (
    DivisionByZeroError,
    EvalOverflow,
    eval_expr,
    eval_expr2,
    fold_constants,
)
from expr import Add, Bin, Div, Mul, Num, Num2, Sub
from pretty import render


def test_eval_basic() -> None:
    """Перевірка базових арифметичних операцій ADT."""
    assert eval_expr(Num(5)) == 5
    assert eval_expr(Add(Num(2), Num(3))) == 5
    assert eval_expr(Sub(Num(10), Num(4))) == 6
    assert eval_expr(Mul(Num(2), Num(3))) == 6
    assert eval_expr(Div(Num(8), Num(2))) == 4


def test_eval_nested() -> None:
    """Перевірка вкладених рекурсивних структур."""
    # ((2 + 3) * (10 - 2)) / 4 = (5 * 8) / 4 = 10
    ast = Div(Mul(Add(Num(2), Num(3)), Sub(Num(10), Num(2))), Num(4))
    assert eval_expr(ast) == 10


def test_render() -> None:
    """Перевірка форматування виразу у рядок."""
    ast = Div(Mul(Add(Num(2), Num(3)), Num(4)), Sub(Num(9), Num(7)))
    assert render(ast) == "(((2 + 3) * 4) / (9 - 7))"


def test_division_by_zero() -> None:
    """Перевірка захисту від ділення на нуль."""
    ast = Div(Num(10), Sub(Num(3), Num(3)))
    with pytest.raises(DivisionByZeroError):
        eval_expr(ast)


def test_overflow() -> None:
    """Перевірка винятку при переповненні MAX_ABS."""
    ast = Mul(Num(5000), Num(3))
    with pytest.raises(EvalOverflow):
        eval_expr(ast)


def test_constant_folding() -> None:
    """Перевірка згортання констант (constant folding)."""
    ast = Mul(Add(Num(2), Num(3)), Sub(Num(10), Num(6)))
    folded = fold_constants(ast)
    assert folded == Num(20)

    div_zero_ast = Div(Add(Num(1), Num(2)), Num(0))
    assert fold_constants(div_zero_ast) == Div(Num(3), Num(0))


def test_eval_expr2_literal() -> None:
    """Перевірка альтернативного AST із Literal-операторами."""
    ast = Bin(
        "/", Bin("*", Bin("+", Num2(2), Num2(3)), Num2(4)), Bin("-", Num2(6), Num2(4))
    )
    assert eval_expr2(ast) == 10
