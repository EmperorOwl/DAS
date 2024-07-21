from backend.operations.graph_operation import GraphOperation


class GraphParametricOperation(GraphOperation):

    def __init__(self, xt: str, yt: str, t_start: str, t_end: str) -> None:
        super().__init__(None, None)
        self.raw_xt = xt
        self.raw_yt = yt
        self.raw_t_start = t_start
        self.raw_t_end = t_end
        self.xt = None
        self.yt = None
        self.t_start = None
        self.t_end = None

    def parse(self) -> None:
        self.xt = self.parser.parse_expr(self.raw_xt)
        self.yt = self.parser.parse_expr(self.raw_yt)
        self.t_start = self.parser.parse_expr(self.raw_t_start)
        self.t_end = self.parser.parse_expr(self.raw_t_end)

    def process(self) -> None:
        self.raw_res = self.api.plot_parametric(self.xt,
                                                self.yt,
                                                (self.VAR.T,
                                                 self.t_start,
                                                 self.t_end),
                                                show=False)

    def render(self) -> None:
        legend = [f'$x(t) = {self.latex(self.xt)}$, '
                  f'$y(t) = {self.latex(self.yt)}$']
        self._render(self.raw_res, legend)

    def print(self) -> None:
        self.pretty_res = (f"Equations: "
                           f"`x(t)={self.pretty(self.xt)}`, "
                           f"`y(t)={self.pretty(self.yt)}`\n"
                           f"Restriction: "
                           f"`t∈[{self.pretty(self.t_start)},"
                           f"{self.pretty(self.t_end)}]`")
