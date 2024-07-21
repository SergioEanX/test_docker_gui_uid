#!/bin/bash

# Run pytest and capture the result
pytest /app/tests/test_main.py
TEST_RESULT=$?

# Exit with the result of the tests
exit $TEST_RESULT
