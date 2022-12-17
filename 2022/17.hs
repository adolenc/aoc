-- https://adventofcode.com/2022/day/17
import Data.List
import qualified Data.Set as S

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

-- dropRock :: [(Int, Int)] -> [String] -> String -> ([(Int, Int)], String)
dropRock shape rockMap jet = let (pos, jet') = restingPosition (spawn shape) jet
                             in (S.union pos rockMap, jet')
  where
    spawn shape = let shapeHeight = maximum (map snd (S.toList shape))
                      rockMapHeight = 1 + maximum (-1:map snd (S.toList rockMap))
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


main = do
  inp <- filter (`elem` "<>") <$> getContents
  let jet = cycle inp
  let rocks = cycle $ map parseShape shapes
  let rockMap = S.empty
  let (rockMap', _) = foldl' (\(rockMap, jet) (r, _) -> dropRock r rockMap jet) (rockMap, jet) (zip rocks [0..2022-1])
  print $ 1 + maximum (-1:map snd (S.toList rockMap'))
  -- let (rockMap'', _) = foldl' (\(rockMap, jet) (r, _) -> dropRock r rockMap jet) (rockMap, jet) (zip rocks [0..1000000000000-1])
  -- print $ 1 + maximum (-1:map snd (S.toList rockMap''))
