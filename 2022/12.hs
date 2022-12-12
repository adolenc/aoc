-- https://adventofcode.com/2022/day/12
import Data.List
import Data.Char
import Data.Maybe
import GHC.Ix
import Data.Graph.AStar (aStar)
import qualified Data.HashSet as H


main = do
  inp <- lines <$> getContents
  let (maxX,maxY) = (length (head inp) - 1,length inp - 1)
      start = head [(x,y) | x <- [0..maxX], y <- [0..maxY], inp!!y!!x == 'S']
      end   = head [(x,y) | x <- [0..maxX], y <- [0..maxY], inp!!y!!x == 'E']
      hmap = map (map (\c -> if c == 'S' then 'a' else if c == 'E' then 'z' else c)) inp
      at (x,y) = hmap!!y!!x
      constCost = const . const
      heightAt = ord . at
  let canMove p n = inRange ((0,0), (maxX,maxY)) n && heightAt n - heightAt p <= 1
      ns p@(x,y) = H.fromList $ filter (canMove p) [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
      Just path = aStar ns (constCost 1) ((heightAt end -) . heightAt) (== end) start
  print (length path)
  let canMove p n = inRange ((0,0), (maxX,maxY)) n && heightAt n - heightAt p >= -1
      ns p@(x,y) = H.fromList $ filter (canMove p) [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
      Just path = aStar ns (constCost 1) heightAt ((== 'a') . at) end
  print (length path)
