-- https://adventofcode.com/2022/day/23
import Data.List
import qualified Data.Set as S

n = (0,-1)
s = (0,1)
e = (1,0)
w = (-1,0)
ne = (1,-1)
nw = (-1,-1)
se = (1,1)
sw = (-1,1)

suggestions = [(n, [n, ne, nw]), (s, [s, se, sw]), (w, [w, nw, sw]), (e, [e, ne, se])]
full = ((0,0), [n, s, w, e, ne, nw, se, sw])

makeIteration :: S.Set (Int, Int) -> [((Int, Int), [(Int,Int)])] -> S.Set (Int, Int)
makeIteration m s = S.fromList . map (`makeMove` dupeMoves) $ S.toList m
  where
    proposedMoves = map proposeMove $ S.toList m
    dupeMoves = S.fromList $ proposedMoves \\ nub proposedMoves
    proposeMove (x,y) = let moves = full : s
                            ((dx,dy):_) = (map fst . filter (\(_, ds) -> not . any (\(dx,dy) -> S.member (x+dx, y+dy) m) $ ds) $ moves) ++ [(0,0)]
                        in (x+dx, y+dy)
    makeMove p dupes = let p' = proposeMove p
                       in if p' `S.notMember` dupes
                          then p'
                          else p

main = do
  inp <- lines <$> getContents
  let m = S.fromList . map fst . filter ((/= '.') . snd) $ concatMap (\(y,row) -> map (\(x,c) -> ((x,y), c)) (zip [0..] row)) (zip [0..] inp)
  let m' = foldl' (\m i -> makeIteration m (take 4 $ drop i $ cycle suggestions)) m [0..10-1]
  let minX = minimum $ map fst $ S.toList m'
  let maxX = maximum $ map fst $ S.toList m'
  let minY = minimum $ map snd $ S.toList m'
  let maxY = maximum $ map snd $ S.toList m'
  print ((maxX - minX + 1) * (maxY - minY + 1) - S.size m')
  let ms' = scanl' (\(m,_) i -> (makeIteration m (take 4 . drop i . cycle $ suggestions), i+1)) (m,0) [0..]
      Just (_, (_,i)) = find (\((m,_), (m',_)) -> m == m') $ zip ms' (tail ms')
  print i
