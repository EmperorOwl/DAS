from abc import ABC

from backend.operations.graph_operation import GraphOperation


class GraphFuncOperation(GraphOperation, ABC):
    """ Represents an abstract graph operation that involves plotting
    functions with respect to a domain and range.
    """

    def parse(self) -> None:
        # Check domain
        if self.raw_dom is not None:
            self.dom = self.parser.parse_lim(self.raw_dom)
        else:
            self.dom = self.DEFAULT_LIMIT
        # Check range
        if self.raw_ran is not None:
            self.ran = self.parser.parse_lim(self.raw_ran)
        else:
            pass  # Range will be automatically calculated.
