from __future__ import annotations

from eval_ import DivisionByZeroError, eval_expr, fold_constants
from expr import Add, Div, Mul, Num, Sub
from pretty import render


def main() -> None:
    print("Лабораторна №8: Алгебраїчні типи даних (Варіант 1)")

    # Вираз: ((10 - 2) * (3 + 0)) / 4
    ast = Div(
        Mul(Sub(Num(10), Num(2)), Add(Num(3), Num(0))),
        Num(4),
    )

    print(f"Початковий вираз : {render(ast)}")
    print(f"Результат обчисл.: {eval_expr(ast)}")

    folded = fold_constants(ast)
    print(f"Після згортання  : {render(folded)} (тип вузла: {type(folded).__name__})")

    bad_ast = Div(Num(42), Sub(Num(5), Num(5)))
    print(f"Небезпечний вираз: {render(bad_ast)}")
    try:
        eval_expr(bad_ast)
    except DivisionByZeroError as err:
        print(f"Перехоплено помилку: {err}")


if __name__ == "__main__":
    main()
