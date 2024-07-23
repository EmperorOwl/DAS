from backend.operations.algebraic_operation import AlgebraicOperation


class ExpandOperation(AlgebraicOperation):

    def process(self) -> None:
        self.raw_res = self.api.expand(self.expr)

    def print(self) -> None:
        self.pretty_res = f"Expanded: `{self.pretty(self.raw_res)}`"
