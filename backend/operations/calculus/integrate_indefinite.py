from ..calculus_operation import CalculusOperation


class IntegrateIndefiniteOperation(CalculusOperation):

    def process(self) -> None:
        self.raw_res = self.api.integrate(self.expr, self.var)

    def render(self) -> None:
        self._render("$"
                     f"\\int \\ ({self.latex(self.expr)}) \\ "
                     f"{{d{self.var}}} = "
                     f"{self.latex(self.raw_res)} + C"
                     "$")

    def print(self) -> None:
        self.pretty_res = (f"Original: `{self.pretty(self.expr)}`\n"
                           f"Indefinite Integral: `{self.pretty(self.raw_res)}`")
