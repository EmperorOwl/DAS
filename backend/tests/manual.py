""" Example code for manipulating the backend. """

from backend import calculator, plotter

if __name__ == '__main__':
    res = calculator.solve('sin(x)=1', 'x')
    print(res)

    plotter.plot_single_func('x^2', 'x')
