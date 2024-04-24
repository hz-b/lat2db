#!/bin/sh
#------------------------------------------------------------
# Author:  Waheedulah Sulaiman Khail
# Date: September 2023
#------------------------------------------------------------

T_DIR=`pwd`/`dirname $0`
T_DIR=`dirname $0`
VENV_DIR="$T_DIR"/../env

# activate the enivronement ... how to do that safely?
. "$VENV_DIR"/bin/activate

# should not be required ... but bether to be explicit
PYTHON="$VENV_DIR"/bin/python3
MAIN="$T_DIR/main.py"

if [ ! -x $PYTHON ]
then
    echo "WARNING: $PYTHON is not executable: still proceeding"
    echo "         keep fingers crossed ..."
fi

if [ ! -f $MAIN ]
then
    echo "WARNING: $MAIN is not found: still proceeding"
    echo "         keep fingers crossed ..."
fi

${PYTHON} ${MAIN}