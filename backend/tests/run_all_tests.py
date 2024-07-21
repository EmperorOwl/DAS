import unittest
import sys
import os


def run_all_tests(test_dir):
    # Discover all tests in the specified directory
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Exit with a status code based on the test results
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    # The directory containing the tests can be specified as an argument
    # If not specified, use the current directory
    if len(sys.argv) > 1:
        test_directory = sys.argv[1]
    else:
        test_directory = os.getcwd()

    run_all_tests(test_directory)
