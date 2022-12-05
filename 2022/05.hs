-- https://adventofcode.com/2022/day/5
import Data.List


parseContents :: String -> ([String], [(Int, Int, Int)])
parseContents contents =
  let (a, _:b) = break (== "") $ lines contents
      readMove (_:moveCount:_:moveFrom:_:moveTo:_) = (read moveCount, read moveFrom - 1, read moveTo - 1)
      readStacks = map (reverse . filter (`elem` ['A'..'Z'])) . filter ((/= ' ') . head) . transpose . reverse
  in (readStacks a, readMove . words <$> b)

main = do
  (stacks, moves) <- parseContents <$> getContents
  let makeMove craneUsed stack (moveCount, moveFrom, moveTo) =
        let crates = take moveCount (stack!!moveFrom)
            manipulate s rid f = map (\(id,row) -> if id == rid then f row else row) (zip [0..] s)
            stack'  = manipulate stack moveFrom (drop moveCount)
            stack'' = manipulate stack' moveTo (craneUsed crates ++)
        in stack''
  print (map head $ foldl' (makeMove reverse) stacks moves)
  print (map head $ foldl' (makeMove id) stacks moves)
