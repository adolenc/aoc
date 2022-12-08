-- https://adventofcode.com/2022/day/8
import Data.Char
import Data.List
import Data.Tuple
import qualified Data.Set as S


allThatSeeStart :: [Int] -> [Int]
allThatSeeStart row = allThatSeeStart' (zip row [0..]) (-1)
  where
    allThatSeeStart' :: [(Int, Int)] -> Int -> [Int]
    allThatSeeStart' [] _ = []
    allThatSeeStart' ((r,i):ris) currentMax | currentMax < r = i : allThatSeeStart' ris r
                                            | otherwise = allThatSeeStart' ris currentMax

takeWhileP1 p xs = map snd (takeWhile fst (zip (True:map p xs) xs))

scenicScore :: Int -> Int -> [[Int]] -> Int
scenicScore x y m = product $ map (length . takeWhileP1 (< m!!y!!x) . map (\(y',x') -> m!!y'!!x')) [above, below, left, right]
  where
    below = zip [y+1..length m-1] (repeat x)
    above = zip (reverse [0..y-1]) (repeat x)
    right = zip (repeat y) [x+1..length (head m)-1]
    left  = zip (repeat y) (reverse [0..x-1])


main = do
  inp <- map (map digitToInt) . lines <$> getContents
  print $ length $ S.fromList
          [co (y, x) | (ci, f, tr, co) <- [(id,        id,      (:[]),                             id),
                                           (id,        reverse, \e -> [length inp - e - 1],        id),
                                           (transpose, id,      (:[]),                             swap),
                                           (transpose, reverse, \e -> [length (head inp) - e - 1], swap)],
                       (y, row) <- zip [0..] (ci inp),
                       x <- allThatSeeStart (f row) >>= tr]
  print $ maximum [scenicScore x y inp | y <- [0..length inp - 1], x <- [0..length (head inp) - 1]]
