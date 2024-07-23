from backend.operations.algebraic_operation import AlgebraicOperation


class SimplifyOperation(AlgebraicOperation):

    def process(self) -> None:
        self.raw_res = self.api.simplify(self.expr)

    def print(self) -> None:
        self.pretty_res = f"Simplified: `{self.pretty(self.raw_res)}`"
