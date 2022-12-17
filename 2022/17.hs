-- https://adventofcode.com/2022/day/17
import Data.List
import Data.Maybe
import qualified Data.Set as S
import Debug.Trace

shapes = [
          ["@@@@"],

          ["_@_",
           "@@@",
           "_@_"],

          ["__@",
           "__@",
           "@@@"],

          ["@",
           "@",
           "@",
           "@"],

          ["@@",
           "@@"]
         ]

parseShape :: [String] -> S.Set (Int, Int)
parseShape shape = S.fromList
                    [(x, height-y-1) | (y, row) <- zip [0..] shape,
                                       (x, c) <- zip [0..] row,
                                       c == '@',
                                       let height = length shape]

printMap m = mapM_ putStrLn $ reverse [[if S.member (x, y) m then '@' else '_' | x <- [0..6]] | y <- [0..height]]
  where
    height = 1 + maximum (map snd $ S.toList m)

height m = 1 + maximum (-1:map snd (S.toList m))

-- dropRock :: [(Int, Int)] -> [String] -> String -> ([(Int, Int)], String)
dropRock i shape rockMap jet = let (pos, jet') = restingPosition (spawn shape) jet
                             in (modifyRockMap pos rockMap, jet')
  where
    spawn shape = let shapeHeight = maximum (map snd (S.toList shape))
                      rockMapHeight = height rockMap
                      shape' = S.map (\(x, y) -> (x+2, y + rockMapHeight + 3)) shape
                  in shape'
    applyJet d shape = let shape' = S.map (\(x, y) -> (x + (if d == '<' then -1 else 1), y)) shape
                       in if any (\(x, y) -> x < 0 || x > 6 || (x, y) `S.member` rockMap) (S.toList shape')
                          then shape
                          else shape'
    moveDown shape = let shape' = S.map (\(x, y) -> (x, y - 1)) shape
                     in if any (\(x, y) -> y < 0 || (x, y) `S.member` rockMap) (S.toList shape')
                        then Nothing
                        else Just shape'
    restingPosition shape (j:et) = let shape' = applyJet j shape
                                   in case moveDown shape' of
                                     Just shape'' -> restingPosition shape'' et
                                     Nothing -> (shape', et)
    modifyRockMap shape rockMap = let ys = nub . map snd $ S.toList shape
                                      rockMap' = S.union rockMap shape
                                  in case find (isEntireRowFilled rockMap') ys of
                                     Just filledY -> --trace ("Yes entire row is filled at i=" ++ show i ++ " and y=" ++ show filledY ++ ", h=" ++ show (height rockMap') ++ " elems: " ++ show (length rockMap')) $
                                                     S.filter (\(x, y) -> y >= filledY) rockMap'
                                     Nothing -> rockMap'
      where
        isEntireRowFilled rockMap y = all (\x -> (x, y) `S.member` rockMap) [0..7-1]


main = do
  inp <- filter (`elem` "<>") <$> getContents
  let jet = cycle inp
      rocks = cycle $ map parseShape shapes
      rockMap = S.empty
      (rockMap', _) = foldl' (\(rockMap, jet) (r, i) -> dropRock i r rockMap jet) (rockMap, jet) (zip rocks [1..2022])
  print $ height rockMap'

  -- basically, between rock #2447 (height 3777) and rock #4177 (height 6436) (deltas #1730 and h=2656) the pattern starts repeating,
  -- so we can just pretend that its the same at rock # (1000000000000 - 4177) // 1730, or, alternatively, that
  -- we just need to simulate (1000000000000 - 4177) % 1730 number of rocks from that point on and see how high
  -- we get. 
  -- I don't know how to nicely spot the repeating pattern - I got insanely lucky noticing this in my trace output
  -- so I'm just leaving the (commented out) trace in the code. I'm sure if I spent a bit more time I could figure out how to get
  -- the pattern programatically. But as is, I'm just simulating 5000 rocks and checking the last two generated maps
  -- that have the length of 1022 (aka 1022 rocks to compare against after pruning step) and assuming those are the bounds
  -- of the repeating pattern. Seems to work.
  --
  -- Still counts as solving it if I just solve it for my specific input right? :D
  let rocksToSimulateToSpotAPattern = 5000
      patternBorderNumberOfElements = 1022
      rockMaps = zip [1..rocksToSimulateToSpotAPattern] $ scanl' (\(rockMap, jet) (r, i) -> dropRock i r rockMap jet) (rockMap, jet) (zip rocks [1..rocksToSimulateToSpotAPattern])
      patternStartingRockMaps = filter (\(r, (m, j)) -> length m == patternBorderNumberOfElements) (reverse rockMaps)
      ((r',m',h',j'):(r,m,h,j):_) = map (\(r,(m,j)) -> (r, m, height m, j)) patternStartingRockMaps
      rocksInAPattern = r' - r
      patternHeight = h' - h
      patternRepetitions = (1000000000000 - r') `div` rocksInAPattern
      heightAtLastPatternRepetition = h' + patternHeight * patternRepetitions
      stillNeedToSimulate = (1000000000000 - r') `mod` rocksInAPattern
      (finalRockMap, _) = foldl' (\(rockMap, jet) (r, i) -> dropRock i r rockMap jet) (m', j') (zip rocks [0..stillNeedToSimulate])
      heightAtEnd = heightAtLastPatternRepetition + (height finalRockMap - h')
  -- To find the rocksToSimulateToSpotAPattern and patternBorderNumberOfElements, run this and pray you can discover some repeating pattern:
  -- if you can't, increase rocksToSimulateToSpotAPattern and try again
  -- print $ map (\(i,(m,j)) -> length m) rockMaps
  print heightAtEnd
