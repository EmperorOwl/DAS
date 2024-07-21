from ..calculus_operation import CalculusOperation


class IntegrateDefiniteOperation(CalculusOperation):

    def __init__(self, expr: str, var: str, lt: str, ut: str) -> None:
        super().__init__(expr, var)
        self.raw_lt = lt
        self.raw_ut = ut
        self.lt = None
        self.ut = None

    def parse(self) -> None:
        super().parse()
        self.lt = self.parser.parse_expr(self.raw_lt)
        self.ut = self.parser.parse_expr(self.raw_ut)

    def process(self) -> None:
        self.raw_res = self.api.integrate(self.expr,
                                          (self.var, self.lt, self.ut))

    def render(self) -> None:
        self._render("$"
                     f"\\int_{{{self.latex(self.lt)}}}^"
                     f"{{{self.latex(self.ut)}}} \\ "
                     f"({self.latex(self.expr)}) \\ "
                     f"{{d{self.var}}} = "
                     f"{self.latex(self.raw_res)}"
                     "$")

    def print(self) -> None:
        self.pretty_res = f"Definite Integral: `{self.pretty(self.raw_res)}`"
