-- https://adventofcode.com/2022/day/16
import Text.ParserCombinators.ReadP
import qualified Data.Map as M
import qualified Data.Set as S
import Data.List
import Data.Ord

parse :: String -> (String, (Int, [String]))
parse = fst . head . readP_to_S (do
    string "Valve "
    valve <- many1 get
    string " has flow rate="
    rate <- read <$> many1 get
    choice [string "; tunnels lead to valves ", string "; tunnel leads to valve "]
    tunnels <- sepBy (many1 get) (string ", ")
    eof
    return (valve, (rate, tunnels)))

type Valves = M.Map String (Int, [String])
type Distances = M.Map String [(String, Int)]

distances :: Valves -> String -> [(String, Int)]
distances g start = distances' g [(start, 0)] M.empty
  where
    distances' :: Valves -> [(String, Int)] -> M.Map String Int -> [(String, Int)]
    distances' _ [] m = M.toList m
    distances' g ((node, dist):xs) m =
      if M.member node m
      then distances' g xs m
      else distances' g (xs ++ map (, dist + 1) (snd (g M.! node))) (M.insert node dist m)

-- return [(distance, node, yield)]
possibleYields :: Valves -> Distances -> String -> Int -> [(Int, String, Int)]
possibleYields g d currentNode remainingMinutes = let ds = d M.! currentNode
                                                  in zip3 (map snd ds) (map fst ds) (map (uncurry valveYield) ds)
  where
    valveYield :: String -> Int -> Int
    valveYield valve distance = (remainingMinutes - distance - 1) * fst (g M.! valve)

openValves :: Valves -> Distances -> Int -> String -> Int
openValves g ds remainingMinutes currentNode = openValves' remainingMinutes currentNode S.empty
  where
    openValves' remainingMinutes currentNode alreadyOpen = 
      let ys = filter (\(d, n, y) -> d < remainingMinutes && y > 0 && S.notMember n alreadyOpen) $ possibleYields g ds currentNode remainingMinutes
      in if remainingMinutes <= 0 || null ys
         then 0
         else maximum $ map (\(d, n, y) -> y + openValves' (remainingMinutes - d - 1) n (S.insert n alreadyOpen)) ys

openValvesWithElephant :: Valves -> Distances -> Int -> String -> Int
openValvesWithElephant g ds remainingMinutes currentNode = openValves' remainingMinutes (0, currentNode, 0) (0, currentNode, 0) S.empty
  where
    openValves' remainingMinutes (distanceYToNodeY, targetNodeY, yieldNodeY) (distanceEToNodeE, targetNodeE, yieldNodeE) alreadyOpen = 
      if remainingMinutes <= 0
      then 0
      else let (nsYY, yY, hasNonsYY) = nextValveCandidates distanceYToNodeY targetNodeY yieldNodeY
               (nsEE, yE, hasNonsEE) = nextValveCandidates distanceEToNodeE targetNodeE yieldNodeE
           in if hasNonsYY && hasNonsEE
              then 0
              else yY + yE + maximum (0:[r | nE'@(_, nnE', _) <- nsEE,
                                             nY'@(_, nnY', _) <- nsYY,
                                             let alreadyOpen' = S.insert nnY' (S.insert nnE' alreadyOpen),
                                             nnE' /= nnY',
                                             let r = openValves' (remainingMinutes-1) nY' nE' alreadyOpen'])
      where
        nextValveCandidates distanceToNode targetNode yieldNode =
          let ns = if distanceToNode == 0
                    then filter (\(d, n, y) -> d < remainingMinutes && y > 0 && S.notMember n alreadyOpen) $ possibleYields g ds targetNode remainingMinutes
                    else [(distanceToNode - 1, targetNode, yieldNode)]
              ns' = if null ns then [(-1, "", 0)] else ns
              y = if distanceToNode == 0 then yieldNode else 0
          in (ns', y, null ns)


main = do
  inp <- map parse . lines <$> getContents
  let g = M.fromList inp
  let ds = M.fromList $ map (\n -> (n, distances g n)) (M.keys g)
  print $ openValves g ds 30 "AA"
  print $ openValvesWithElephant g ds 26 "AA"
