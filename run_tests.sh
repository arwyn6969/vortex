#!/bin/bash

# Install test dependencies
pip install -e ".[test]"

# Run tests with coverage
python -m pytest

# Open coverage report if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open htmlcov/index.html
fi 