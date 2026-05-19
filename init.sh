#!/bin/bash

# Find virtual environment python executable
VENV_PYTHON=""
if [ -f ".venv/bin/python" ]; then
    VENV_PYTHON=".venv/bin/python"
elif [ -f "venv/bin/python" ]; then
    VENV_PYTHON="venv/bin/python"
fi

if [ -n "$VENV_PYTHON" ]; then
    $VENV_PYTHON scripts/validate_harness.py "$@"
else
    if command -v python3 >/dev/null 2>&1; then
        python3 scripts/validate_harness.py "$@"
    else
        python scripts/validate_harness.py "$@"
    fi
fi
exit $?
