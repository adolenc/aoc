-- https://adventofcode.com/2022/day/2

score "A X" = 1 + 3
score "A Y" = 2 + 6
score "A Z" = 3 + 0
score "B X" = 1 + 0
score "B Y" = 2 + 3
score "B Z" = 3 + 6
score "C X" = 1 + 6
score "C Y" = 2 + 0
score "C Z" = 3 + 3

stratScore "A X" = 0 + 3
stratScore "A Y" = 3 + 1
stratScore "A Z" = 6 + 2
stratScore "B X" = 0 + 1
stratScore "B Y" = 3 + 2
stratScore "B Z" = 6 + 3
stratScore "C X" = 0 + 2
stratScore "C Y" = 3 + 3
stratScore "C Z" = 6 + 1


main = do
  inp <- lines <$> getContents
  print (sum $ map score inp)
  print (sum $ map stratScore inp)


---- Alternative solution
-- import Data.List
-- import Data.Maybe
--
-- data Move = Rock | Paper | Scissors deriving (Show, Eq)
--
-- toMove "A" = Rock
-- toMove "B" = Paper
-- toMove "C" = Scissors
-- toMove "X" = Rock
-- toMove "Y" = Paper
-- toMove "Z" = Scissors
--
-- Paper `beats` Rock = True
-- Scissors `beats` Paper = True
-- Rock `beats` Scissors = True
-- _ `beats` _ = False
--
-- moveScore Rock = 1
-- moveScore Paper = 2
-- moveScore Scissors = 3
--
-- score [x, y] | x `beats` y = 0 + moveScore y
--              | x == y      = 3 + moveScore y
--              | y `beats` x = 6 + moveScore y
--
-- stratScore [x, y] = case [x, y] of
--   [x, "X"] -> 0 + moveScore $ moveSuchThat (xm `beats`)
--   [x, "Y"] -> 3 + moveScore $ moveSuchThat (== xm)
--   [x, "Z"] -> 6 + moveScore $ moveSuchThat (`beats` xm)
--   where
--     xm = toMove x
--     moveSuchThat p = fromJust $ find p [Rock, Paper, Scissors]
--
--
-- main = do
--   inp <- getContents
--   print (sum $ map score $ map (map toMove . words) $ lines inp)
--   print (sum $ map stratScore $ map words $ lines inp)
