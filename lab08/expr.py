from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias, Union

Op: TypeAlias = Literal["+", "-", "*", "/"]


class SupportsBinaryOp(Protocol):
    """Структурний контракт (Protocol) для бінарних вузлів AST."""

    @property
    def op(self) -> Op: ...

    @property
    def left(self) -> Expr: ...

    @property
    def right(self) -> Expr: ...


@dataclass(frozen=True)
class Num:
    value: int


@dataclass(frozen=True)
class Add:
    left: Expr
    right: Expr
    op: Literal["+"] = "+"


@dataclass(frozen=True)
class Sub:
    left: Expr
    right: Expr
    op: Literal["-"] = "-"


@dataclass(frozen=True)
class Mul:
    left: Expr
    right: Expr
    op: Literal["*"] = "*"


@dataclass(frozen=True)
class Div:
    left: Expr
    right: Expr
    op: Literal["/"] = "/"


@dataclass(frozen=True)
class Bin:
    """Альтернативний бінарний вузол із явним використанням Literal Op."""

    op: Op
    left: Expr2
    right: Expr2


@dataclass(frozen=True)
class Num2:
    value: int


Expr: TypeAlias = Union[Num, Add, Sub, Mul, Div]  # noqa: UP007
Expr2: TypeAlias = Union[Num2, Bin]  # noqa: UP007
