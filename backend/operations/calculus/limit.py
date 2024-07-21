from ..calculus_operation import CalculusOperation


class LimitOperation(CalculusOperation):

    def __init__(self, expr: str, var: str, val: str) -> None:
        super().__init__(expr, var)
        self.raw_val = val
        self.val = None

    def parse(self) -> None:
        super().parse()
        self.val = self.parser.parse_expr(self.raw_val)

    def process(self) -> None:
        self.raw_res = self.api.limit(self.expr, self.var, self.val)

    def render(self) -> None:
        self._render("$"
                     f"\\lim_{{{self.var} \\rightarrow "
                     f"{self.latex(self.val)}}} "
                     f"({self.latex(self.expr)}) = "
                     f"{self.latex(self.raw_res)}"
                     "$")

    def print(self) -> None:
        self.pretty_res = f"Limit: `{self.pretty(self.raw_res)}`"
