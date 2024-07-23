from backend.operations.algebraic_operation import AlgebraicOperation


class EvaluateOperation(AlgebraicOperation):
    MAX = 100_000_000_000

    def process(self) -> None:
        self.raw_res = self.expr.evalf()
        if self.raw_res > self.MAX:
            self.raw_res = float('inf')
        elif self.raw_res < -self.MAX:
            self.raw_res = float('-inf')

    def print(self) -> None:
        self.pretty_res = f"Answer: `{self.pretty(self.raw_res)}`"
