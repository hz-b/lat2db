#!/bin/sh
#------------------------------------------------------------
# Author:  Waheedulah Sulaiman Khail
# Date: September 2023
#------------------------------------------------------------
PYTHON=/usr/bin/python3
T_DIR=`dirname $0`
MAIN="$T_DIR/main.py"

if [ ! -x $PYTHON ]
then
    echo "WARNING: $PYTHON is not executable: still proceeding"
    echo "         keep finges crossed ..."
fi

if [ ! -f $MAIN ]
then
    echo "WARNING: $MAIN is not found: still proceeding"
    echo "         keep finges crossed ..."
fi

${PYTHON} ${MAIN}
