from abc import ABC

from backend.operations.algebraic_operation import AlgebraicOperation


class CalculusOperation(AlgebraicOperation, ABC):
    """ Represents an abstract math operation related to calculus that
    performs some calculation on an expression with respect to a variable.
    """

    def __init__(self, expr: str, var: str) -> None:
        super().__init__(expr)
        self.raw_var = var
        self.var = None

    def parse(self) -> None:
        super().parse()
        self.var = self.parser.parse_var(self.raw_var)
