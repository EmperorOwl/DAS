import sympy
from typing import Any
from abc import ABC, abstractmethod

from backend import parser, printer
from backend.utils import Set, Var


class Operation(ABC):
    """ Represents an abstract operation. """
    SET = Set
    VAR = Var

    def __init__(self) -> None:
        """ Creates a new operation. """
        self.raw_res = None
        self.pretty_res = None
        self.parser = parser
        self.api = sympy

    @staticmethod
    def latex(expr) -> str:
        """ Converts the expression expr to a LaTeX string representation. """
        return sympy.latex(expr)

    @staticmethod
    def pretty(obj: Any) -> str:
        """ Returns the pretty print of the Sympy object obj. """
        return printer.pretty(obj)

    @abstractmethod
    def parse(self) -> None:
        """ Validates the inputs of the operation. """
        pass

    @abstractmethod
    def process(self) -> None:
        """ Initialises the raw result of the operation. """
        pass

    @abstractmethod
    def render(self) -> None:
        """ Converts the raw result of the operation to a PNG image. """
        pass

    @abstractmethod
    def print(self) -> None:
        """ Initialises the pretty result of the operation. """
        pass

    def execute(self) -> (str, str):
        """ Executes all the steps in the operation. """
        self.parse()
        self.process()
        self.render()
        self.print()
        return self.pretty(self.raw_res), self.pretty_res
