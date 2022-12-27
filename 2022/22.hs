-- https://adventofcode.com/2022/day/22
import Text.ParserCombinators.ReadP
import qualified Data.Map as M
import Data.List
import Debug.Trace
import Data.Char


data Move = RotateR | RotateL | Forward Int
  deriving (Show, Eq)

type RockMap = M.Map (Int, Int) Char

parse :: String -> ((RockMap, (Int, Int)), [Move])
parse i = ((mm, (maxX,maxY)), parseDir dd)
  where
    (m, _:[dd]) = break null $ lines i
    (maxX, maxY) = (maximum $ map length m, length m)
    mm = M.fromList $ filter ((/= ' ') . snd) $ concatMap (\(y,row) -> map (\(x,c) -> ((x,y), c)) (zip [0..] row)) (zip [0..] m)
    parseDir = fst . head . readP_to_S (do
        let d = choice [string "R" *> return RotateR, string "L" *> return RotateL, Forward . read <$> munch1 isDigit]
        z <- many1 d
        eof
        return z)

(x1, y1) %+ (x2, y2) = (x1 + x2, y1 + y2)
(x, y) %* n = (x * n, y * n)

modPlus (x1, y1) (x2, y2) (maxX,maxY) = ((x1 + x2 + maxX) `mod` maxX, (y1 + y2 + maxY) `mod` maxY)

faceDir :: Move -> (Int, Int) -> (Int, Int)
faceDir RotateL (dx, dy) = (dy, -dx)
faceDir RotateR (dx, dy) = (-dy, dx)
faceDir (Forward _) d = d

makeMove :: Move -> (Int, Int) -> (Int, Int) -> (RockMap, (Int, Int)) -> (Int, Int)
makeMove (Forward 1) d p (m,dmax) =
  let p' = head . dropWhile (`M.notMember` m) . tail $ iterate (\p -> modPlus p d dmax) p
  in case M.lookup p' m of
       Just '.' -> p'
       Just '#' -> p
makeMove (Forward n) d p m = foldl' (\p' _ -> makeMove (Forward 1) d p' m) p [1..n]
makeMove _ _ p _ = p

-- transitionExample :: (Int, Int) -> (Int, Int) -> ((Int, Int), (Int, Int))
-- transitionExample p@(x,y) d@(dx,dy) = go (toCubeIndex p) (toCubeIndex p')
--   where
--     p'@(x',y') = p %+ d
--     c@(cx,cy) = (x `mod` 4, y `mod` 4)
--     toCubeIndex (x, y) = (((x `div` 4) + 6) `mod` 6, ((y `div` 4) + 6) `mod` 6)
--     go (2,1) (3,1) = ((3,2) %* 4 %+ (3-cy, 0), (0, 1))
--     go (2,2) (2,3) = ((0,1) %* 4 %+ (3-cx, 3), (0,-1))
--     go (1,1) (1,0) = ((2,0) %* 4 %+ (0, cx), (1,0))
--     go a b = error ("Trying to move somewhere not covered: " ++ show a ++ " => " ++ show b) (p, d)

--  0,0  [1,0] [2,0]
--  0,1  [1,1]  2,1
-- [0,2] [1,2]  2,2
-- [0,3]  1,3   2,3
transitionCube :: (Int, Int) -> (Int, Int) -> ((Int, Int), (Int, Int))
transitionCube p@(x,y) d@(dx,dy) = -- trace ("transitioning: go "  ++ show (toCubeIndex p) ++ " " ++ show p ++ " " ++ show d ++ " -> " ++ show (go (toCubeIndex p) d)) $
  go (toCubeIndex p) d
  where
    c@(cx,cy) = (x `mod` 50, y `mod` 50)
    toCubeIndex (x, y) = (((x `div` 50) + 6) `mod` 6, ((y `div` 50) + 6) `mod` 6)

    go (1,1) (1,0) = ((2,0) %* 50 %+ (cy, 49), (0,-1))
    go (2,0) (0,1) = ((1,1) %* 50 %+ (49, cx), (-1,0))

    go (1,2) (1,0) = ((2,0) %* 50 %+ (49, 49-cy), (-1,0))
    go (2,0) (1,0) = ((1,2) %* 50 %+ (49, 49-cy), (-1,0))

    go (0,3) (1,0) = ((1,2) %* 50 %+ (cy, 49), (0,-1))
    go (1,2) (0,1) = ((0,3) %* 50 %+ (49, cx), (-1,0))

    go (1,0) (-1,0) = ((0,2) %* 50 %+ (0, 49-cy), (1,0))
    go (0,2) (-1,0) = ((1,0) %* 50 %+ (0, 49-cy), (1,0))

    go (0,3) (0,1) = ((2,0) %* 50 %+ (cx,0), (0,1))
    go (2,0) (0,-1) = ((0,3) %* 50 %+ (cx, 49), (0,-1))

    go (0,3) (-1,0) = ((1,0) %* 50 %+ (cy, 0), (0,1))
    go (1,0) (0,-1) = ((0,3) %* 50 %+ (0,cx), (1,0))

    go (1,1) (-1,0) = ((0,2) %* 50 %+ (cy,0), (0,1))
    go (0,2) (0,-1) = ((1,1) %* 50 %+ (0,cx), (1,0))
    go a b = error ("Trying to move somewhere not covered: go " ++ show a ++ " " ++ show d) (p, d)

makeMoveAroundCube :: Move -> (Int, Int) -> (Int, Int) -> RockMap -> ((Int, Int), (Int, Int))
makeMoveAroundCube (Forward 1) d p m =
  let (p',d') = if M.member (p %+ d) m then (p %+ d, d) else transitionCube p d
  in case M.lookup p' m of
       Just '.' -> (d', p')
       Just '#' -> (d, p)
makeMoveAroundCube (Forward n) d p m = foldl' (\(d', p') _ -> makeMoveAroundCube (Forward 1) d' p' m) (d, p) [1..n]
makeMoveAroundCube _ d p _ = (d, p)

main = do
  ((inpMap, inpMax), inpMoves) <- parse <$> getContents
  let (x, y) = minimum . filter (\(x,y) -> y == 0) . M.keys $ inpMap
  let (d',(x',y')) = foldl' (\(d, p) m -> let d' = faceDir m d
                                              p' = makeMove m d' p (inpMap, inpMax)
                                          in (d', p'))
                            ((1,0), (x,y))
                            inpMoves
  let dScores = M.fromList [((1,0), 0), ((0,1), 1), ((-1,0), 2), ((0,-1), 3)]
  print $ (y'+1) * 1000 + (x'+1) * 4 + (dScores M.! d')
 
  let (d',(x',y')) = foldl' (\(d, p) m -> let d' = faceDir m d
                                              (d'',p') = makeMoveAroundCube m d' p inpMap
                                          in (d'', p'))
                            ((1,0), (x,y))
                            inpMoves
  print $ (y'+1) * 1000 + (x'+1) * 4 + (dScores M.! d')
