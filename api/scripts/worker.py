""" Code for the worker process. """
import sys
import json

from scripts.algebra import *
from scripts.calculus import *
from scripts.graphs import *
from scripts.solvers import *
from scripts.misc import *
from scripts.utils import Error


def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            operation = req.get("operation")
            args = req.get("args", {})
            func = globals().get(operation)
            if callable(func):
                output = func(args).__dict__
            else:
                output = Error(
                    name="UnknownOperation",
                    message=f"Unknown operation: {operation}",
                ).__dict__
        except Exception as e:
            output = Error(name=type(e).__name__, message=str(e)).__dict__
        print(json.dumps(output), flush=True)


if __name__ == "__main__":
    main()
