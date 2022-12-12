-- https://adventofcode.com/2022/day/12
import Data.List
import Data.Char
import Data.Maybe
import GHC.Ix
import Data.Graph.AStar (aStar)
import qualified Data.HashSet as H


dist :: (Int, Int) -> (Int, Int) -> Int
dist (x1,y1) (x2,y2) = abs (x1-x2) + abs (y1-y2)

main = do
  inp <- lines <$> getContents
  let (maxX,maxY) = (length (head inp) - 1,length inp - 1)
      start = head [(x,y) | x <- [0..maxX], y <- [0..maxY], inp!!y!!x == 'S']
      end   = head [(x,y) | x <- [0..maxX], y <- [0..maxY], inp!!y!!x == 'E']
      hmap = map (map (\c -> if c == 'S' then 'a' else if c == 'E' then 'z' else c)) inp
      at (x,y) = hmap!!y!!x
      constCost = const . const
  let ok p@(x,y) pn@(xn,yn) = inRange ((0,0), (maxX,maxY)) (xn,yn) && (ord $ at pn) - (ord $ at p) <= 1
      ns (x,y) = H.fromList $ filter (ok (x,y)) [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
      Just path = aStar ns (constCost 1) (dist end) (== end) start
  print (length path)
  let ok p@(x,y) pn@(xn,yn) = inRange ((0,0), (maxX,maxY)) (xn,yn) && (ord $ at pn) - (ord $ at p) >= -1
      ns (x,y) = H.fromList $ filter (ok (x,y)) [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
      Just path = aStar ns (constCost 1) (ord . at) (\p -> at p == 'a') end
  print (length path)
