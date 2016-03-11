#!/bin/bash
PYTHONPATH="${PYTHONPATH}:$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/mudd"
export PYTHONPATH
# run compiler
python3 mudd/frontdesk.py ${BASH_ARGV[0]}
