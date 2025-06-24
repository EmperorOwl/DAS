import unittest
import sys
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # Discover all tests in the current directory
    loader = unittest.TestLoader()
    suite = loader.discover(CURR_DIR)

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())
