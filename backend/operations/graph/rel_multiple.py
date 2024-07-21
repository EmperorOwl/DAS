from backend.operations.graph_operation import GraphOperation


class GraphMultipleRelOperation(GraphOperation):
    COLOR1 = 'darkorange'
    COLOR2 = 'darkslateblue'

    def __init__(self, rel1: str, rel2: str, dom: str, ran: str) -> None:
        super().__init__(dom, ran)
        self.raw_rel1 = rel1
        self.raw_rel2 = rel2
        self.rel1 = None
        self.rel2 = None

    def parse(self) -> None:
        super().parse()
        self.rel1 = self.parser.parse_rel(self.raw_rel1)
        self.rel2 = self.parser.parse_rel(self.raw_rel2)

    def process(self) -> None:
        plot1 = self.api.plot_implicit(self.rel1,
                                       (self.VAR.X,) + self.dom,
                                       (self.VAR.Y,) + self.ran,
                                       show=False,
                                       line_color=self.COLOR1,
                                       xlabel=None,
                                       ylabel=None,
                                       xlim=self.dom,
                                       ylim=self.ran)
        plot2 = self.api.plot_implicit(self.rel2,
                                       (self.VAR.X,) + self.dom,
                                       (self.VAR.Y,) + self.ran,
                                       show=False,
                                       line_color=self.COLOR2,
                                       xlabel=None,
                                       ylabel=None,
                                       xlim=self.dom,
                                       ylim=self.ran)
        plot1.append(plot2[0])
        self.raw_res = plot1

    def render(self) -> None:
        legend = [f'${self.latex(self.rel1)}$',
                  f'${self.latex(self.rel2)}$']
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Relations: "
                           f"`{self.pretty(self.rel1)}, "
                           f"{self.pretty(self.rel2)}`\n"
                           f"Limits: `x∈{self.dom}`, `y∈{self.ran}`")
