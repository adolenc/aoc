-- https://adventofcode.com/2022/day/20
import Data.List


main = do
  inp <- zip [0..] . map (read :: String->Int) . lines <$> getContents
  let rotateTo i xs = drop i xs ++ take i xs
      moveHead ((id,x):xs) = let p = x `mod` length xs
                                 p' = if p < 0 then p + length xs else p
                             in take p' xs ++ [(id,x)] ++ drop p' xs
      findN n xs = let Just i = findIndex (\(id,x) -> id == n) xs
                   in rotateTo i xs
      mixup is = foldl' (\xs id -> moveHead $ findN id xs) is [0..length is - 1]
      result r = let rs = map snd r
                     Just i = elemIndex 0 rs
                 in sum $ map (\n -> rotateTo i rs !! (n `mod` length rs)) [1000, 2000, 3000]
  print (result $ mixup inp)
  let decryptedList = map (\(id,x) -> (id, x * 811589153)) inp
      r' = foldl' (\xs _ -> mixup xs) decryptedList [1..10]
  print (result r')
