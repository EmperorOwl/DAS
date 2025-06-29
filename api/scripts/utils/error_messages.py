""" Error messages for the parser. """


def invalid_character(char: str):
    return f"{char} is an invalid character"


def invalid_input(s: str):
    return f"{s} is invalid"


def no_latex():
    return "Please do not use \\ and note latex input is not accepted"


def invalid_factorial():
    return "Only one (!) and double (!!) factorial are allowed"


def invalid_syntax(right: str, wrong: str):
    return f"Please use {right} instead of {wrong}"


def missing_closing_bracket(s: str):
    return f"{s} is probably missing a closing bracket"


def only_one_argument(func: str):
    return f"{func}() requires 1 argument"


def invalid_log():
    return "log() requires 2 arguments\n" \
           "log(n, b) returns the logarithm of n to base b\n" \
           "e.g. log(10, 2) computes the logarithm of 10 to base 2\n" \
           "the default base is the natural base, e"


def invalid_root():
    return "root() requires 2 arguments\n" \
           "root(n, k) returns the kth root of n\n" \
           "e.g. root(8, 3) computes the cube root of 8"


def invalid_mod():
    return "mod() requires 2 arguments\n" \
           "mod(n, k) returns the remainder when n is divided by k\n" \
           "e.g. mod(5, 2) computes 5 mod 2"
