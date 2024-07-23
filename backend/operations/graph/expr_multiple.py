from backend.operations.graph_operation import GraphOperation


class GraphMultipleExprOperation(GraphOperation):

    def __init__(self, expr1: str, expr2: str, dom: str, ran: str) -> None:
        super().__init__(dom, ran)
        self.raw_expr1 = expr1
        self.raw_expr2 = expr2
        self.expr1 = None
        self.expr2 = None

    def parse(self) -> None:
        super().parse()
        self.expr1 = self.parser.parse_expr(self.raw_expr1)
        self.expr2 = self.parser.parse_expr(self.raw_expr2)

    def process(self) -> None:
        self.raw_res = self.api.plotting.plot3d(self.expr1,
                                                self.expr2,
                                                (self.VAR.X,) + self.dom,
                                                (self.VAR.Y,) + self.ran,
                                                show=False)

    def render(self) -> None:
        legend = [f'$f1(x,y) = {self.latex(self.expr1)}$',
                  f'$f2(x,y) = {self.latex(self.expr2)}$']
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Expressions: "
                           f"`{self.pretty(self.expr1)}, "
                           f"{self.pretty(self.expr2)}`\n"
                           f"Limits: `x∈{self.dom}`, `y∈{self.ran}`")
