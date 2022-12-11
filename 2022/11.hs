-- https://adventofcode.com/2022/day/11
import Data.Ord
import Data.List
import Data.List.Split
import qualified Data.Map as M


paragraphs :: [String] -> [[String]]
paragraphs = foldr f [[]]
  where
    f "" acc = []:acc
    f x (y:ys) = (x:y):ys

data Monkey = Monkey { items :: [Int]
                     , operation :: [String]
                     , testDivisor :: Int
                     , trueCaseMonkeyId :: Int
                     , elseCaseMonkeyId :: Int
                     , inspectionCount :: Int }
  deriving (Show)

parseMonkey :: [String] -> Monkey
parseMonkey lines = Monkey items operation testDivisor trueCaseMonkeyId elseCaseMonkeyId 0
  where
    items = map read . splitOn ", " . last . splitOn ": " $ lines!!1
    operation = words . last . splitOn " = " $ lines!!2
    testDivisor = read . last . words $ lines!!3
    trueCaseMonkeyId = read . last . words $ lines!!4
    elseCaseMonkeyId = read . last . words $ lines!!5

evalMonkeyOp :: [String] -> Int -> Int
evalMonkeyOp operation item = parseOp operation
  where
    parseOp ["old", op, "old"] = evalOp op item item
    parseOp ["old", op, a] = evalOp op item (read a)
    parseOp [a, op, "old"] = evalOp op (read a) item
    parseOp [a, op, b] = evalOp op (read a) (read b)
    evalOp "+" a b = a + b
    evalOp "*" a b = a * b

simulateMonkey :: (Int -> Int) -> M.Map Int Monkey -> Int -> M.Map Int Monkey
simulateMonkey worryFn state id = foldl' simulateMonkey' state (items (state M.! id))
  where 
    simulateMonkey' state item =
      let monkey = (state M.! id)
          res = worryFn $ evalMonkeyOp (operation monkey) item
          trueMonkey = (state M.! trueCaseMonkeyId monkey)
          elseMonkey = (state M.! elseCaseMonkeyId monkey)
          state' = M.insert id (monkey { items = tail (items monkey), inspectionCount = 1 + inspectionCount monkey }) state
      in if res `mod` testDivisor monkey == 0
         then M.insert (trueCaseMonkeyId monkey) (trueMonkey {items = items trueMonkey ++ [res]}) state'
         else M.insert (elseCaseMonkeyId monkey) (elseMonkey {items = items elseMonkey ++ [res]}) state'

simulateRound :: (Int -> Int) -> M.Map Int Monkey -> M.Map Int Monkey
simulateRound worryFn state = foldl' (simulateMonkey worryFn) state (M.keys state)

main = do
  inp <- map parseMonkey . paragraphs . lines <$> getContents
  let state = M.fromList . zip [0..] $ inp
  let monkeyBusiness = product . take 2 . sortOn Down . M.elems . M.map inspectionCount
  print (monkeyBusiness $ foldl' (\s _ -> simulateRound (`div` 3) s) state [1..20])
  let worry = product $ M.elems $ M.map testDivisor state
  print (monkeyBusiness $ foldl' (\s _ -> simulateRound (`mod` worry) s) state [1..10000])
