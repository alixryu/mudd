#!/bin/bash
PYTHONPATH="${PYTHONPATH}:$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/mudd"
export PYTHONPATH
# run scanner
python3 mudd/scanner.py ${BASH_ARGV[0]}
