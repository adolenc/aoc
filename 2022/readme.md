AoC 2022
========

My solutions for [Advent of Code 2022](https://adventofcode.com/2022), in
Haskell. Every solution is in its own individual file that reads puzzle's input
via standard input and prints two lines (one per star) to standard output.

For solving I use `./dev.sh ${day?}`, which generates a template Haskell file
`$day.hs` and a blank `in` file for the puzzle input. The script then uses
[entr](https://eradman.com/entrproject/) to re-run the solution whenever any of
these two files are written to.

External dependencies required to run some of the solutions:

    $ cabal install --lib split astar
