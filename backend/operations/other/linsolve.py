from backend.operations.math_operation import MathOperation


class LinsolveOperation(MathOperation):

    def __init__(self, equations: list[str], variables: list[str]) -> None:
        super().__init__()
        self.raw_eqs = equations
        self.raw_vars = variables
        self.eqs = None
        self.vars = None

    def parse(self) -> None:
        self.eqs = [self.parser.parse_eq(eq) for eq in self.raw_eqs
                    if eq is not None]
        self.vars = [self.parser.parse_var(var) for var in self.raw_vars
                     if var is not None]

    def process(self) -> None:
        self.raw_res = self.api.linsolve(self.eqs, self.vars)

    def render(self) -> None:
        # Equation has no sols.
        if isinstance(self.raw_res, self.SET.EMPTY):
            self._render("No solution")
        # Equations has finite sols.
        else:
            sols = self.raw_res.args[0]
            tex = ""
            for i in range(len(sols)):
                tex += f"{self.vars[i]} = {self.latex(sols[i])}"
                if i < len(sols) - 1:
                    tex += '|'  # Will be converted to ", "
            self._render(f'${tex}$')

    def print(self) -> None:
        self.pretty_res = "Equations: "
        self.pretty_res += ", ".join(f"`{self.pretty(eq)}`"
                                     for eq in self.eqs)
        self.pretty_res += "\n"
        self.pretty_res += "Solutions: "
        # Equation has no sols.
        if isinstance(self.raw_res, self.SET.EMPTY):
            self.pretty_res += "`∅`"
        # # Equations has finite sols.
        else:
            sols = self.raw_res.args[0]
            self.pretty_res += ", ".join(f"`{var}={self.pretty(sol)}`"
                                         for var, sol in zip(self.vars, sols))
