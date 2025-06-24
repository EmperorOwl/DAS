""" Code for the worker process. """
import sys
import json

from scripts.algebra import *
from scripts.calculus import *
from scripts.graphs import *
from scripts.solvers import *
from scripts.misc import *


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
                output = {"error": f"Unknown operation: {operation}"}
        except Exception as e:
            output = {"error": str(e)}
        print(json.dumps(output), flush=True)


if __name__ == "__main__":
    main()
