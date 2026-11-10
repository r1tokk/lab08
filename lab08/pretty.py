from __future__ import annotations

from typing import Protocol

from expr import Add, Div, Expr, Mul, Num, Sub, SupportsBinaryOp


class Renders(Protocol):
    """Протокол для об'єктів, що підтримують текстовий рендер."""

    def render(self) -> str: ...


def format_binary_op(node: SupportsBinaryOp) -> str:
    """Допоміжна функція, що працює через структурний контракт SupportsBinaryOp."""
    return f"({render(node.left)} {node.op} {render(node.right)})"


def render(e: Expr) -> str:
    """Перетворює арифметичне дерево у відформатований рядок через match/case."""
    match e:
        case Num(value=v):
            return str(v)
        case Add() | Sub() | Mul() | Div() as bin_node:
            return format_binary_op(bin_node)
