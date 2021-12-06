#!/usr/bin/env bash

if [ ! -f $1.py ]; then
  cat <(echo "# https://adventofcode.com/2021/day/$1") template.py > $1.py
  > in
fi
nvim-qt in $1.py -- -o
ls $1.py in | entr -s "python3 $1.py < in; date"
