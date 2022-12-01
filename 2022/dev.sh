#!/usr/bin/env bash

if [ ! -f $1.hs ]; then
  echo -e "-- https://adventofcode.com/2022/day/$1\n\n\nmain = do\n  inp <- getContents\n  " > $1.hs
  > in
fi
kitty -e -- nvim in $1.hs -o &
ls $1.hs in | entr -s "runghc $1.hs < in; date"
