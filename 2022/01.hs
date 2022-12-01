-- https://adventofcode.com/2022/day/1
import Data.List

paragraphs :: [String] -> [[String]]
paragraphs = foldr f [[]]
  where
    f "" acc = []:acc
    f x (y:ys) = (x:y):ys

main = do
  inp <- getContents
  let calories = map (map read) $ paragraphs $ lines inp
  let sums = map sum calories
  print (maximum sums)
  print (sum $ take 3 . reverse . sort $ sums)
