-- https://adventofcode.com/2022/day/19
import Data.Char
import Control.Monad.Trans.State
import qualified Data.Set as S


data Cost = C { ore :: Int, clay :: Int, obsidian :: Int, geode :: Int }
  deriving (Show, Eq, Ord)
data Blueprint = Blueprint { oreRobot :: Cost, clayRobot :: Cost, obsidianRobot :: Cost, geodeRobot :: Cost }
  deriving (Show, Eq, Ord)

(%>=) :: Cost -> Cost -> Bool
C o1 c1 o2 c2 %>= C o3 c3 o4 c4 = o1 >= o3 && c1 >= c3 && o2 >= o4 && c2 >= c4

(%+) :: Cost -> Cost -> Cost
C o1 c1 o2 c2 %+ C o3 c3 o4 c4 = C (o1 + o3) (c1 + c3) (o2 + o4) (c2 + c4)

(%-) :: Cost -> Cost -> Cost
C o1 c1 o2 c2 %- C o3 c3 o4 c4 = C (o1 - o3) (c1 - c3) (o2 - o4) (c2 - c4)

parseBlueprint :: String -> Blueprint
parseBlueprint l = let i = words l
                   in Blueprint
                     (C (read (i!!6)) 0 0 0)
                     (C (read (i!!12)) 0 0 0)
                     (C (read (i!!18)) (read (i!!21)) 0 0)
                     (C (read (i!!27)) 0 (read (i!!30)) 0)

findBestOutcome' :: Blueprint -> Cost -> Cost -> Int -> State Int Int
findBestOutcome' blueprint wallet bots timeLeft =
  if timeLeft == 0
  then return $ geode wallet
  else let botAddedValues = [C 0 0 0 1, C 0 0 1 0, C 0 1 0 0, C 1 0 0 0]
           botCosts = [geodeRobot blueprint, obsidianRobot blueprint, clayRobot blueprint, oreRobot blueprint]
           stillNeedMoreBots = [True, obsidian bots < maximum (map obsidian botCosts), clay bots < maximum (map clay botCosts), ore bots < maximum (map ore botCosts)]
           canCreate = map (\(c,p,_) -> (c,p)) $ filter (\(c, p, s) -> s && wallet %>= c) (zip3 botCosts botAddedValues stillNeedMoreBots)
           maximumPossibleGeodes = max ((timeLeft - 1) * (timeLeft - 2) `div` 2) 0 + geode wallet + (geode bots * timeLeft)
           canCreate' = if canCreate == [(geodeRobot blueprint, C 0 0 0 1)] then canCreate else canCreate ++ [(C 0 0 0 0, C 0 0 0 0)]
       in do
            memodBest <- gets id
            if memodBest > maximumPossibleGeodes
            then return memodBest
            else do
              outcomes <- mapM (\(c, p) -> findBestOutcome' blueprint (wallet %+ bots %- c) (bots %+ p) (timeLeft - 1)) canCreate'
              let bestOutcome = maximum outcomes
              modify (const (max memodBest bestOutcome))
              return (max memodBest bestOutcome)

findBestOutcome blueprint wallet bots timeLeft = evalState (findBestOutcome' blueprint wallet bots timeLeft) 0


main = do
  inp <- map parseBlueprint . lines <$> getContents
  print . sum . map (\(id, bp) -> findBestOutcome bp (C 0 0 0 0) (C 1 0 0 0) 24 * id) $ zip [1..] inp
  print . product . map (\bp -> findBestOutcome bp (C 0 0 0 0) (C 1 0 0 0) 32) $ take 3 inp
