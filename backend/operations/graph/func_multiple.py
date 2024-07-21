from backend.operations.graph_func_operation import GraphFuncOperation


class GraphMultipleFuncOperation(GraphFuncOperation):
    COLOR1 = 'lightskyblue'
    COLOR2 = 'lightgreen'

    def __init__(self, f1: str, f2: str, var: str, dom: str, ran: str) -> None:
        super().__init__(dom, ran)
        self.raw_f1 = f1
        self.raw_f2 = f2
        self.raw_var = var
        self.f1 = None
        self.f2 = None

    def parse(self) -> None:
        super().parse()
        self.f1 = self.parser.parse_func(self.raw_f1, self.raw_var)
        self.f2 = self.parser.parse_func(self.raw_f2, self.raw_var)

    def process(self) -> None:
        plot = self.api.plot(self.f1.expr,
                             self.f2.expr,
                             (self.f1.var,) + self.dom,
                             show=False,
                             xlabel=None,
                             ylabel=None,
                             xlim=self.dom,
                             ylim=self.ran)
        plot[0].line_color = self.COLOR1
        plot[1].line_color = self.COLOR2
        self.raw_res = plot

    def render(self) -> None:
        legend = [self.f1.get_latex(), self.f2.get_latex()]
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Functions: `{self.f1}`, `{self.f2}`\n"
                           f"Limits: `{self.f1.var}∈{self.dom}`")
        if self.ran:
            self.pretty_res += f", `{self.f1.name},{self.f2.name}∈{self.ran}`"
