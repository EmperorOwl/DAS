from ..calculus_operation import CalculusOperation


class DeriveOperation(CalculusOperation):

    def process(self) -> None:
        self.raw_res = self.api.diff(self.expr, self.var)

    def render(self) -> None:
        self._render("$"
                     f"\\frac{{d}}{{d{self.var}}} "
                     f"({self.latex(self.expr)}) = "
                     f"{self.latex(self.raw_res)}"
                     "$")

    def print(self) -> None:
        self.pretty_res = (f"Original: `{self.pretty(self.expr)}`\n"
                           f"Derivative: `{self.pretty(self.raw_res)}`")
