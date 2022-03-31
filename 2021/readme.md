AoC 2021
========

My solutions for [Advent of Code 2021](https://adventofcode.com/2021), in
Python 3. Every solution is in its own individual file that reads puzzle's input
via standard input and prints two lines (one per star) to standard output.

For solving I use `./dev.sh ${day?}`, which generates a template python file
`$day.py` and a blank `in` file for the puzzle input. The script then uses
[entr](https://eradman.com/entrproject/) to re-run the solution whenever any of
these two files are written to.

Executing `./runall.sh ${SESSION_TOKEN?}` runs all the solutions in order by
downloading the inputs from the advent of code website.
