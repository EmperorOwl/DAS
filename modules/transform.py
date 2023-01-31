""" Code for transforming and validating user input. """

from __future__ import annotations

import typing

import discord

from backend import parser
from backend.parser import sp_obj


class Limit(typing.NamedTuple):
    """ Represents a limit either a domain or range.

    attributes:
        lower: the lower bound of the domain or range
        upper: the upper bound of the domain or range

    """
    lower: float
    upper: float

    @classmethod
    async def transform(cls, _, val: str) -> Limit:
        """ Returns the transformed domain or range as a tuple. """
        for char in ['(', ')', '[', ']']:
            val = val.replace(char, '')
        (x, _, y) = val.partition(',')
        # Check for valid.
        if y:
            return cls(lower=int(x.strip()), upper=int(y.strip()))
        raise Exception("Invalid Limit")

    def __str__(self) -> str:
        """ Returns the pretty print. """
        return f"({self.lower}, {self.upper})"


DEFAULT_LIMIT = Limit(-5, 5)


class Function(typing.NamedTuple):
    """ Represents a function which consists of its name and parsed expression.

    attributes:
        name: the name of the function
        expr: the parsed expression

    """
    name: str
    expr: sp_obj

    @classmethod
    async def transform(cls, _, val: str) -> Function:
        """ Returns the transformed function. """
        if 'y' in val or ('x' not in val and 't' not in val):
            raise Exception("Not A Function")
        name, expr = parser.split(val)
        return cls(name, expr)

    def __str__(self) -> str:
        """ Returns the pretty print. """
        return f"{self.name} = {self.expr}"


class Relation(typing.Generic[sp_obj]):
    """ Represents a parsed relation. """

    @classmethod
    async def transform(cls, _, val: str) -> Relation:
        """ Returns the parsed expression. """
        if 'x' not in val and 'y' not in val:
            raise Exception("Not An Relation")
        return parser.parse(val)


class Expression(typing.Generic[sp_obj]):
    """ Represents a parsed expression. """

    @classmethod
    async def transform(cls, itx: discord.Interaction, val: str) -> Expression:
        """ Returns the parsed expression. """
        if itx.command.name != 'calculate' and '=' in val:
            raise Exception("Not An Expression")
        return parser.parse(val)


class Equation(typing.Generic[sp_obj]):
    """ Represents a parsed equation. """

    @classmethod
    async def transform(cls, _, val: str) -> Equation:
        """ Returns the parsed expression. """
        return parser.parse(val)
