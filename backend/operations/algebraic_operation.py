from abc import ABC

from backend.operations.math_operation import MathOperation


class AlgebraicOperation(MathOperation, ABC):
    """ Represents an abstract math operation which performs some algebraic
    calculation on an expression.
    """

    def __init__(self, expr: str) -> None:
        super().__init__()
        self.raw_expr = expr
        self.expr = None

    def parse(self) -> None:
        self.expr = self.parser.parse_expr(self.raw_expr)

    def render(self) -> None:
        self._render(f"${self.latex(self.expr)} = "
                     f"{self.latex(self.raw_res)}$")
