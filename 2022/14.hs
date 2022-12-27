-- https://adventofcode.com/2022/day/14
import Data.List
import Data.List.Split
import qualified Data.Set as S


type RockMap = S.Set (Int, Int)

toRockMap :: String -> RockMap
toRockMap = toMap . parseInput 
  where
    parseInput = map (map ((\(x:y:_) -> (read x, read y)) . splitOn ",") . splitOn " -> ") . lines
    toMap = foldl' toMap' S.empty
    toMap' m ((x,y):(x',y'):ps) = let rocks = S.fromList [(x,y) | x <- [min x x'..max x x'], y <- [min y y'..max y y']]
                                  in toMap' (S.union m rocks) ((x',y'):ps)
    toMap' m [p] = S.insert p m

dropSand :: Int -> RockMap -> Maybe RockMap
dropSand abyss = dropSand' (500,0)
  where
    dropSand' (x,y) m | S.member (500,0) m = Nothing
                      | y >= abyss = Nothing
                      | S.notMember   (x,y+1) m = dropSand'   (x,y+1) m
                      | S.notMember (x-1,y+1) m = dropSand' (x-1,y+1) m
                      | S.notMember (x+1,y+1) m = dropSand' (x+1,y+1) m
                      | otherwise = Just $ S.insert (x,y) m

-- https://stackoverflow.com/a/35749543
iterateMaybe f = unfoldr (fmap (\s -> (s,s)) . f)

main = do
  inp <- toRockMap <$> getContents
  let abyss = maximum . map snd $ S.toList inp
  print (length $ iterateMaybe (dropSand abyss) inp)
  let abyssFloor = S.fromList $ map (, abyss+2) [500-abyss*2..500+abyss*2]
  print (length $ iterateMaybe (dropSand (abyss + 10)) $ S.union inp abyssFloor)
