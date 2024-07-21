from backend.operations.graph_func_operation import GraphFuncOperation


class GraphSingleFuncOperation(GraphFuncOperation):
    COLOR = 'lightskyblue'

    def __init__(self, func: str, var: str, dom: str, ran: str) -> None:
        super().__init__(dom, ran)
        self.raw_func = func
        self.raw_var = var
        self.func = None

    def parse(self) -> None:
        super().parse()
        self.func = self.parser.parse_func(self.raw_func, self.raw_var)

    def process(self) -> None:
        self.raw_res = self.api.plot(self.func.expr,
                                     (self.func.var,) + self.dom,
                                     show=False,
                                     line_color=self.COLOR,
                                     xlabel=None,
                                     ylabel=None,
                                     xlim=self.dom,
                                     ylim=self.ran)

    def render(self) -> None:
        legend = [self.func.get_latex()]
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Function: `{self.func}`\n"
                           f"Limits: `{self.func.var}∈{self.dom}`")
        if self.ran:
            self.pretty_res += f", `{self.func.name}∈{self.ran}`"
