from backend.operations.graph_operation import GraphOperation


class GraphSingleExprOperation(GraphOperation):

    def __init__(self, expr: str, dom: str, ran: str) -> None:
        super().__init__(dom, ran)
        self.raw_expr = expr
        self.expr = None

    def parse(self) -> None:
        super().parse()
        self.expr = self.parser.parse_expr(self.raw_expr)

    def process(self) -> None:
        self.raw_res = self.api.plotting.plot3d(self.expr,
                                                (self.VAR.X,) + self.dom,
                                                (self.VAR.Y,) + self.ran,
                                                show=False)

    def render(self) -> None:
        legend = [f'$f(x,y)={self.latex(self.expr)}$']
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Expression: `{self.pretty(self.expr)}`\n"
                           f"Limits: `x∈{self.dom}`, `y∈{self.ran}`")
