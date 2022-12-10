-- https://adventofcode.com/2022/day/10
import Data.List


chunks :: Int -> [a] -> [[a]]
chunks n [] = []
chunks n xs = take n xs:chunks n (drop n xs)

main = do
  inp <- map words . lines <$> getContents
  let (_,v) = foldl' (\(x, xs) i ->
                        case i of
                          ["addx", v] -> (x + read v, x:x:xs)
                          ["noop"]    -> (x, x:xs))
                     (1, [])
                     inp
  print (sum [x * c | (c, x) <- zip [1..] (reverse v), (c + 20) `mod` 40 == 0])
  mapM_ putStrLn $ chunks 40 [px | (crt, spritex) <- zip [1..240] (reverse v),
                                   let sx = spritex `mod` 40,
                                   let crtx = (crt-1) `mod` 40,
                                   let px = if abs (sx - crtx) <= 1 then '#' else '.']
