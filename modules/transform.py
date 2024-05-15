""" Code for transforming and validating user input. """

from __future__ import annotations

import typing
import discord

from backend import parser
from backend.parser import sp_obj
from modules.bot import DAS


class CTR(Exception):
    """ Represents a Custom Transformer Error. """
    pass  # Used to change the error message in the error handler.


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
            return cls(lower=float(x.strip()), upper=float(y.strip()))
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
    async def transform(cls, itx: discord.Interaction, val: str) -> Function:
        """ Returns the transformed function. """
        kwargs = DAS.get_original_inputs(itx)
        if itx.command.qualified_name == 'graph parametric equations':
            variable = 't'
        else:
            variable = kwargs.get('variable', kwargs.get('var'))
        # Attempt to parse the value entered,
        name, expr = parser.split(func=val, var=variable)
        # Check that variable is in function.
        if variable not in str(expr) and not str(expr).isnumeric():
            raise CTR("Failed to find Variable in Function")
        # Finally, return the Function object.
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
            raise CTR("Failed to find x or y in Relation")
        return parser.parse(val)


class Expression(typing.Generic[sp_obj]):
    """ Represents a parsed expression. """

    @classmethod
    async def transform(cls, itx: discord.Interaction, val: str) -> Expression:
        """ Returns the parsed expression. """
        if itx.command.name != 'calculate' and '=' in val:
            raise CTR("Expression cannot contain equal signs")
        return parser.parse(val)


class Equation(typing.Generic[sp_obj]):
    """ Represents a parsed equation. """

    @classmethod
    async def transform(cls, _, val: str) -> Equation:
        """ Returns the parsed expression. """
        return parser.parse(val)


class Value(typing.Generic[sp_obj]):
    """ Represents a value. """

    @classmethod
    async def transform(cls, _, val: str) -> Value:
        """ Returns the parsed expression. """
        for char in ['=', '<', '>']:
            if char in val:
                raise CTR("Value cannot contain relational operators")
        return parser.parse(val)


class Vector(typing.NamedTuple):
    """ Represents a vector.

    attributes:
        x: the horizontal component
        y: the vertical component

    """
    x: float
    y: float

    @classmethod
    async def transform(cls, _, val: str) -> Vector:
        """ Returns the vector. """
        for char in ['(', ')', '[', ']']:
            val = val.replace(char, '')
        x, y = val.split(',')
        return cls(float(x.strip()), float(y.strip()))

    def __str__(self) -> str:
        """ Returns the pretty print. """
        return f"({self.x:g}, {self.y:g})"


DEFAULT_ORIGIN = Vector(0.0, 0.0)
