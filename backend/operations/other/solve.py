from backend.operations.math_operation import MathOperation


class SolveOperation(MathOperation):

    def __init__(self, eq: str, var: str, dom: str) -> None:
        super().__init__()
        self.raw_eq = eq
        self.raw_var = var
        self.raw_dom = dom
        self.eq = None
        self.var = None
        self.dom = None

    def parse(self) -> None:
        self.eq = self.parser.parse_eq(self.raw_eq)
        self.var = self.parser.parse_var(self.raw_var)
        self.dom = self.parser.parse_dom(self.raw_dom)

    def process(self) -> None:
        self.raw_res = self.api.solveset(self.eq, self.var, self.dom)

    def render(self) -> None:
        # Equation has no sols.
        if isinstance(self.raw_res, self.SET.EMPTY):
            self._render("No solution")
        # Equation has infinite sols over the real domain.
        elif isinstance(self.raw_res, self.SET.REALS):
            self._render(f"${self.var} \\in \\mathbb{{R}}$")
        # Equation has infinite sols over the complex domain.
        elif isinstance(self.raw_res, self.SET.COMPLEXES):
            self._render(f"${self.var} \\in \\mathbb{{C}}$")
        # Equation has interval solution.
        elif isinstance(self.raw_res, self.SET.INTERVAL):
            self._render(f"${self.var} \\in {self.latex(self.raw_res)}$")
        # Otherwise.
        else:
            self._render(f"${self.var} = {self.latex(self.raw_res)}$")

    def print(self) -> None:
        from backend import printer
        # Equation has finite sols.
        if isinstance(self.raw_res, self.SET.FINITE):
            sols_str = ', '.join(f'`{printer.pretty_individual(sol)}`'
                                 for sol in self.raw_res)
        # Equation has infinite sols.
        elif isinstance(self.raw_res, self.SET.UNION | self.SET.INTERSECTION):
            sols_str = ', '.join(f'`{printer.pretty_individual(sol)}`'
                                 for sol in self.raw_res.args)
        else:
            sols_str = f'`{self.pretty(self.raw_res)}`'
        self.pretty_res = (f"Equation: `{self.pretty(self.eq)}`\n"
                           f"Solution: {sols_str}")
