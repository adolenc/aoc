-- https://adventofcode.com/2022/day/18
import Data.List.Split
import Data.List
import qualified Data.Set as S
import Data.Maybe
import Data.Graph.AStar (aStar)
import qualified Data.HashSet as H


-- astar is an insane overkill here and does ridiculous repetition of work,
-- but I figured it was gonna be faster to just use it than writing floodfill or something
nonReachableCubelets :: S.Set (Int, Int, Int) -> [(Int, Int, Int)]
nonReachableCubelets cubelets =
  let edges d = (minimum d, maximum d)
      (minX, maxX) = edges $ map (\(x,_,_) -> x) $ S.toList cubelets
      (minY, maxY) = edges $ map (\(_,y,_) -> y) $ S.toList cubelets
      (minZ, maxZ) = edges $ map (\(_,_,z) -> z) $ S.toList cubelets
      allCubelets = S.fromList [(x,y,z) | x <- [minX..maxX], y <- [minY..maxY], z <- [minZ..maxZ]] S.\\ cubelets
      end = (minX-1,minY-1,minZ-1)
      constCost = const . const
      dist (x1,y1,z1) (x2,y2,z2) = abs (x1-x2) + abs (y1-y2) + abs (z1-z2)
      canMove n = S.notMember n cubelets
      ns p@(x,y,z) = H.fromList $ filter canMove [(x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z), (x,y,z+1), (x,y,z-1)]
      canFindWayOut start = case aStar ns (constCost 1) (dist end) (== end) start of
                              Nothing -> Just start
                              _ -> Nothing
  in mapMaybe canFindWayOut $ S.toList allCubelets

main = do
  inp <- map ((\[x,y,z] -> (read x, read y, read z)::(Int,Int,Int)) . splitOn ",") . lines <$> getContents
  let cubelets = (S.fromList inp)
  let touching cubelets (x,y,z) = length [(x+x',y+y',z+z') | x' <- [-1..1],
                                                             y' <- [-1..1],
                                                             z' <- [-1..1],
                                                             length (filter (==0) [x',y',z']) == 2,
                                                             (x+x',y+y',z+z') `S.member` cubelets]
      surfaceArea cubelets = (6 * length cubelets) - sum (map (touching cubelets) $ S.toList cubelets)
  print $ surfaceArea cubelets
  let holes = nonReachableCubelets cubelets 
      filledCubelets = S.union cubelets (S.fromList holes)
  print $ surfaceArea filledCubelets
