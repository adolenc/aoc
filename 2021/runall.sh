#!/usr/bin/env bash


for day in `seq -w 1 25`; do
  echo "https://adventofcode.com/2021/day/${day#0}"
  curl "https://adventofcode.com/2021/day/${day#0}/input" -X GET -H "Cookie: session=$1" > ${day}_in 2>/dev/null
  python3 ${day}.py < ${day}_in
  sleep 1
done
