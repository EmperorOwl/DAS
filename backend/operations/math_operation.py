from abc import ABC

from backend.operations.operation import Operation
from backend import renderer


class MathOperation(Operation, ABC):
    """ Represents an abstract math operation. """

    @staticmethod
    def _render(tex: str) -> None:
        renderer.render(tex)
