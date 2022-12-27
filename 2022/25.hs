-- https://adventofcode.com/2022/day/25

toDecimal :: String -> Int
toDecimal = toDecimal' . reverse 
  where
    toDecimal' ('2':xs) =  2 + 5 * toDecimal' xs
    toDecimal' ('1':xs) =  1 + 5 * toDecimal' xs
    toDecimal' ('0':xs) =  0 + 5 * toDecimal' xs
    toDecimal' ('-':xs) = -1 + 5 * toDecimal' xs
    toDecimal' ('=':xs) = -2 + 5 * toDecimal' xs
    toDecimal' [] = 0

toSNAFU :: Int -> String
toSNAFU = reverse . toSNAFU'
  where
    toSNAFU' 0 = ""
    toSNAFU' d = case (d+2) `mod` 5 of
                   4 -> '2' : toSNAFU' ((d+2) `div` 5)
                   3 -> '1' : toSNAFU' ((d+2) `div` 5)
                   2 -> '0' : toSNAFU' ((d+2) `div` 5)
                   1 -> '-' : toSNAFU' ((d+2) `div` 5)
                   0 -> '=' : toSNAFU' ((d+2) `div` 5)

main = do
  inp <- lines <$> getContents
  print (toSNAFU . sum . map toDecimal $ inp)
