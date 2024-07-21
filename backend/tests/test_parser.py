from backend import parser

if __name__ == '__main__':
    # Seeing how the SymPy parser handles different inputs
    inputs = [
        # Numbers
        '1', '-1', '0', '9', '123',
        # Basic Operations
        '1+1', '2*2', '5-3', '4/2',
        # Exponents
        '2^3', 'e', 'log',
        # Factorial
        '5!',
        # Trigonometric
        'sin(x)', 'cos(x)', 'tan(x)',
        # Algebraic
        '2*x', '2x', '2x^2', '2x+1',
        'y=x', 'x=y^2',
        # Equations/Relations
        '1 = 1', '2 == 2',
        '1 != 2',
        '2 < 3',
        '7 > 2',
        '4 <= 5',
        '5 >= 6'
    ]
    for s in inputs:
        res = parser._parse(s)
        print(s.ljust(15), str(res).ljust(15), type(res))
