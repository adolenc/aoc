-- https://adventofcode.com/2022/day/24
import Data.List
import qualified Data.Set as S
import qualified Data.HashSet as H
import Data.Graph.AStar (aStar)


main = do
  inp <- lines <$> getContents
  
  let d '>' = (1,0)
      d '<' = (-1,0)
      d '^' = (0,-1)
      d 'v' = (0,1)
      d '#' = (0,0)
  let m = [((x, y), d c) | (y, row) <- zip [0..] inp,
                           (x, c) <- zip [0..] row,
                           c /= '.']
          ++ [((1, -1), (0, 0))]

  let posAtI i ((x,y), (dx,dy)) = if (dx,dy) /= (0,0)
                                  then ((((x-1) + i * dx) `mod` (length (head inp) - 2)) + 1, (((y-1) + i * dy) `mod` (length inp - 2)) + 1)
                                  else (x,y)

  let maps = scanl' (\m' i -> S.fromList (map (posAtI i) m)) (S.fromList (map (posAtI 0) m)) [1..]

  let start = (1, 0)
      end = (length (head inp) - 2, length inp - 1)
      notOccupied i (x,y) = (x,y) `S.notMember` (maps!!i)
      next (p, i) = filter (notOccupied i) [(x + dx, y + dy) | (x, y) <- [p], (dx, dy) <- [(1,0), (-1,0), (0,1), (0,-1), (0,0)]]
      constCost = const . const
      dist (x1,y1) ((x2,y2),_) = abs (x1-x2) + abs (y1-y2)
      ns (p, i) = H.fromList $ zip (next (p, i + 1)) (repeat (i + 1))
      Just path = aStar ns (constCost 1) (dist end) ((==end) . fst) (start, 0)
      (_, d) = last path
  print d

  let Just path' = aStar ns (constCost 1) (dist start) ((==start) . fst) (end, d)
      (_, d') = last path'
      Just path'' = aStar ns (constCost 1) (dist end) ((==end) . fst) (start, d')
      (_, d'') = last path''
  print d''
