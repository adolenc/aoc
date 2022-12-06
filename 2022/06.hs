-- https://adventofcode.com/2022/day/6
import Data.List
import qualified Data.Set as S

substring start length = take length . drop start

main = do
  inp <- getContents
  let Just i = findIndex ((==4) . length) $ map (S.fromList . (\i -> substring i 4 inp)) [0..length inp-1-4]
  print (4 + i)
  let Just i = findIndex ((==14) . length) $ map (S.fromList . (\i -> substring i 14 inp)) [0..length inp-1-14]
  print (14 + i)
