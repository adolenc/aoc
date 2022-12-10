-- https://adventofcode.com/2022/day/9
import qualified Data.Set as S
import Data.List


chebyshev :: (Int, Int) -> (Int, Int) -> Int
chebyshev (x1, y1) (x2, y2) = max (abs (x1 - x2)) (abs (y1 - y2))

makeMove :: (Int, Int) -> Char -> (Int, Int)
makeMove (hx, hy) 'U' = (hx, hy + 1)
makeMove (hx, hy) 'D' = (hx, hy - 1)
makeMove (hx, hy) 'L' = (hx - 1, hy)
makeMove (hx, hy) 'R' = (hx + 1, hy)

forceMove :: (Int, Int) -> (Int, Int) -> (Int, Int)
forceMove h t = if chebyshev h t <= 1 then t else moveTowards t h
  where
    moveTowards (x1, y1) (x2, y2) = (x1 + signum (x2 - x1), y1 + signum (y2 - y1))

propagateMove :: [(Int, Int)] -> [(Int, Int)]
propagateMove [t] = [t]
propagateMove (h:t:ts) = h : propagateMove (forceMove h t:ts)

main = do
  inp <- concatMap ((\[d,c] -> replicate (read c::Int) (head d)) . words) . lines <$> getContents
  let simulate = foldl' (\(trail, h:t) d -> let links' = propagateMove (makeMove h d:t) in (last links':trail, links'))
  print $ length $ S.fromList $ fst $ simulate ([], [(0, 0), (0, 0)]) inp
  print $ length $ S.fromList $ fst $ simulate ([], replicate 10 (0, 0)) inp
