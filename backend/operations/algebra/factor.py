from backend.operations.algebraic_operation import AlgebraicOperation


class FactorOperation(AlgebraicOperation):

    def process(self) -> None:
        self.raw_res = self.api.factor(self.expr)

    def print(self) -> None:
        self.pretty_res = f"Factored: `{self.pretty(self.raw_res)}`"
