-- https://adventofcode.com/2022/day/15
import Data.Char
import Data.List
import Data.List.Split
import GHC.Ix
import Data.Maybe
import qualified Data.Set as S


parseInput :: String -> ((Int, Int), (Int, Int))
parseInput = parseLine . splitOn " "
  where 
    parseLine l = ((readInt (l !! 2), readInt (l !! 3)), (readInt (l !! 8), readInt (l !! 9)))
    readInt = read . filter (\c -> isDigit c || ('-' == c))

manhattan :: (Int, Int) -> (Int, Int) -> Int
manhattan (x1, y1) (x2, y2) = abs (x2 - x1) + abs (y2 - y1)

impossibleBeaconsAtY :: Int -> (Int, Int) -> (Int, Int) -> Maybe (Int, Int)
impossibleBeaconsAtY y s@(sx, sy) b@(bx, by) =
  let distCoverage = manhattan s b
      distToY = abs (y - sy)
  in if distCoverage < distToY
     then Nothing
     else Just (sx - (distCoverage - distToY), sx + (distCoverage - distToY))

unionIntervals :: [(Int, Int)] -> [(Int, Int)]
unionIntervals = go . sort
  where
    go [] = []
    go [a] = [a]
    go (i:j:is) = case i `union` j of
                    Just c -> go (c:is)
                    Nothing -> i : go (j:is)
    union o@(a, b) p@(c, d) = if inRange o c || inRange o d || inRange p a || inRange p b
                               then Just (min a c, max b d)
                               else Nothing

main = do
  inp <- map parseInput . lines <$> getContents
  let y = 2000000
      intervalsAt y = unionIntervals . catMaybes $ map (uncurry $ impossibleBeaconsAtY y) inp
      beaconsAt y = S.fromList . map fst . filter ((== y) . snd) $ map snd inp
  print (((\(x1, x2) -> x2 - x1 + 1) . head $ intervalsAt y) - length (beaconsAt y))
  let Just beaconY = findIndex ((> 1) . length . intervalsAt) [0..4000000]
      ((_,beaconXm1):_) = intervalsAt beaconY
  print ((beaconXm1+1) * 4000000 + beaconY)
