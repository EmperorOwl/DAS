from abc import ABC

from backend.operations.operation import Operation
from backend.core import Limit
from backend import renderer


class GraphOperation(Operation, ABC):
    """ Represents an abstract graph operation that involves plotting with
    respect to a domain and range.
    """
    DEFAULT_LIMIT = Limit(-5, 5)

    def __init__(self, dom: str | None, ran: str | None) -> None:
        super().__init__()
        self.raw_dom = dom
        self.raw_ran = ran
        self.dom = None
        self.ran = None

    @staticmethod
    def _render(plot, legend) -> None:
        renderer.render_plot(plot, legend)

    def parse(self) -> None:
        # Check domain.
        if self.raw_dom is not None:
            self.dom = self.parser.parse_lim(self.raw_dom)
        else:
            self.dom = self.DEFAULT_LIMIT
        # Check range.
        if self.raw_ran is not None:
            self.ran = self.parser.parse_lim(self.raw_ran)
        else:
            self.ran = self.DEFAULT_LIMIT
