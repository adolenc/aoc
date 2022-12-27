-- https://adventofcode.com/2022/day/3
import Data.Char
import Data.List


-- https://stackoverflow.com/a/12882583
chunks n = takeWhile (not . null) . unfoldr (Just . splitAt n)

main = do
  inp <- lines <$> getContents
  let findRepeats r = head $ uncurry intersect $ splitAt (length r `div` 2) r
  let priority c = if c `elem` ['a'..'z'] then ord c - ord 'a' + 1 else ord c - ord 'A' + 27
  print (sum $ map (priority . findRepeats) inp)
  print (sum $ map (priority . head . foldr1 intersect) (chunks 3 inp))
