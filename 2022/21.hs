-- https://adventofcode.com/2022/day/21
import qualified Data.Map as M


data Instruction = Const Int | Op Char String String
    deriving (Show)

(~) = (div)

parseMonkey :: String -> (String, Instruction)
parseMonkey s = (name, instructions)
  where
    (name, ':':' ':rest) = break (== ':') s
    instructions = case words rest of
                     [a, [op], b] -> Op op a b
                     [a] -> Const (read a)

evalMonkey :: Instruction -> M.Map String Instruction -> Int
evalMonkey (Const i) _ = i
evalMonkey (Op '+' a b) ms = evalMonkey (ms M.! a) ms + evalMonkey (ms M.! b) ms
evalMonkey (Op '-' a b) ms = evalMonkey (ms M.! a) ms - evalMonkey (ms M.! b) ms
evalMonkey (Op '*' a b) ms = evalMonkey (ms M.! a) ms * evalMonkey (ms M.! b) ms
evalMonkey (Op '/' a b) ms = evalMonkey (ms M.! a) ms ~ evalMonkey (ms M.! b) ms

has :: String -> String -> M.Map String Instruction -> Bool
has name root monkeys = go (monkeys M.! root)
  where
    go (Const _) = name == root
    go (Op _ a b) = has name a monkeys || has name b monkeys

evalHumn :: Int -> String -> Instruction -> M.Map String Instruction -> Int
evalHumn result "humn" _ _ = result
evalHumn result name (Const i) _ = i
evalHumn result name (Op op a b) ms = 
  let isHumnOnLhs = has "humn" a ms
      (humn, notHumn) = if isHumnOnLhs then (a, b) else (b, a)
      result' = evalMonkey (ms M.! notHumn) ms
  in case op of
       '+' -> evalHumn (result - result') humn (ms M.! humn) ms
       '-' -> if isHumnOnLhs
              then evalHumn (result + result') humn (ms M.! humn) ms
              else evalHumn (-result + result') humn (ms M.! humn) ms
       '*' -> evalHumn (result ~ result') humn (ms M.! humn) ms
       '/' -> if isHumnOnLhs
              then evalHumn (result' * result) humn (ms M.! humn) ms
              else evalHumn (result' ~ result) humn (ms M.! humn) ms

main = do
  inp <- M.fromList . map parseMonkey . lines <$> getContents
  print (evalMonkey (inp M.! "root") inp)
  let Op _ lhs rhs = inp M.! "root"
      (notHumn, humn) = if has "humn" rhs inp then (lhs, rhs) else (rhs, lhs)
      shouldEvalTo = evalMonkey (inp M.! notHumn) inp
  print (evalHumn shouldEvalTo humn (inp M.! humn) inp)
