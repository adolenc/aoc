-- https://adventofcode.com/2022/day/4
import Data.List.Split
import GHC.Utils.Misc
import GHC.Ix


toPairOfRanges :: String -> [[Int]]
toPairOfRanges = map (map read . splitOn "-") . splitOn ","

main = do
  inp <- map toPairOfRanges . lines <$> getContents
  let [a, b] `isContainedIn` [c, d] = a >= c && b <= d
  let isEitherContained [ab, cd] = ab `isContainedIn` cd || cd `isContainedIn` ab
  print (count isEitherContained inp)
  let overlaps [[a, b], [c, d]] = isEitherContained [[a, b], [c, d]] || inRange (c, d) a || inRange (c, d) b
  print (count overlaps inp)
