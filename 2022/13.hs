-- https://adventofcode.com/2022/day/13
import Data.List
import Data.Maybe
import Text.ParserCombinators.ReadP


paragraphs :: [String] -> [[String]]
paragraphs = foldr f [[]]
  where
    f "" acc = []:acc
    f x (y:ys) = (x:y):ys

data Packet = PV Int | PVs [Packet] deriving (Show, Eq)

pList :: ReadP Packet
pList = PVs <$> between (char '[') (char ']') (sepBy (choice [pValue, pList]) (char ','))

pValue :: ReadP Packet
pValue = PV . read <$> munch1 (`elem` ['0'..'9'])

instance Ord Packet where
  compare (PV a) (PV b) | a < b = LT
                   | a > b = GT 
                   | otherwise = EQ
  compare (PVs a) (PV b) = compare (PVs a) (PVs [PV b])
  compare (PV a) (PVs b) = compare (PVs [PV a]) (PVs b)
  compare (PVs (a:as)) (PVs (b:bs)) = case compare a b of
                                  EQ -> compare (PVs as) (PVs bs)
                                  x -> x
  compare (PVs []) (PVs []) = EQ
  compare (PVs []) (PVs _) = LT
  compare (PVs _) (PVs []) = GT

main = do
  inp <- paragraphs . lines <$> getContents
  let toPacket = fst . head . readP_to_S pList
      areInRightOrder [a, b] = compare a b /= GT
  print (sum . map fst . filter snd . zip [1..] $ map (areInRightOrder . map toPacket) inp)
  let p2 = toPacket "[[2]]"
      p6 = toPacket "[[6]]"
      sorted = sort (p2:p6:map toPacket (concat inp))
      (Just p2i, Just p6i) = (elemIndex p2 sorted, elemIndex p6 sorted)
  print ((1 + p2i) * (1 + p6i))
