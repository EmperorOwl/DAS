"""
https://docs.sp.org/latest/modules/solvers/solveset.html
"""
import sympy as sp


class Set:
    """ Contains some Sympy sets. """
    FINITE = sp.sets.sets.FiniteSet
    INTERVAL = sp.sets.sets.Interval
    PRODUCT = sp.sets.sets.ProductSet
    IMAGE = sp.sets.fancysets.ImageSet
    COMPLEX_REGION = sp.sets.fancysets.ComplexRegion
    CONDITION = sp.sets.conditionset.ConditionSet
    NATURALS = sp.sets.fancysets.Naturals
    NATURALS0 = sp.sets.fancysets.Naturals0
    INTEGERS = sp.sets.fancysets.Integers
    REALS = sp.sets.fancysets.Reals
    COMPLEXES = sp.sets.fancysets.Complexes
    EMPTY = sp.sets.sets.EmptySet

    UNION = sp.sets.sets.Union
    INTERSECTION = sp.sets.sets.Intersection
