from backend.operations.graph_operation import GraphOperation


class GraphSingleRelOperation(GraphOperation):
    COLOR = 'darkorange'

    def __init__(self, rel: str, dom: str, ran: str) -> None:
        super().__init__(dom, ran)
        self.raw_rel = rel
        self.rel = None

    def parse(self) -> None:
        super().parse()
        self.rel = self.parser.parse_rel(self.raw_rel)

    def process(self) -> None:
        self.raw_res = self.api.plot_implicit(self.rel,
                                              (self.VAR.X,) + self.dom,
                                              (self.VAR.Y,) + self.ran,
                                              show=False,
                                              line_color=self.COLOR,
                                              xlabel=None,
                                              ylabel=None,
                                              xlim=self.dom,
                                              ylim=self.ran)

    def render(self) -> None:
        legend = [f'${self.latex(self.rel)}$']
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Relation: `{self.pretty(self.rel)}`\n"
                           f"Limits: `x∈{self.dom}`, `y∈{self.ran}`")
