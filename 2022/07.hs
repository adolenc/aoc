-- https://adventofcode.com/2022/day/7
import qualified Data.Map as M
import Data.List.Split
import Data.List


data FD = Directory [FD] | File Int
  deriving (Show)

type Path = [String]
type FileMap = M.Map Path FD

-- uhh this looks bad
toTree :: FileMap -> Path -> FD
toTree m p = case M.lookup p m of
               Just (Directory _) -> Directory $ map (toTree m) $ filter ((p==) . init) $ M.keys m
               Just fd -> fd
               Nothing -> error "not found"

-- and this looks even worse... i bet i could at least make FD an instance of foldable or something
toList :: FD -> [FD]
toList dir@(Directory fs) = dir:concatMap toList fs
toList file = [file]

cmd :: String -> [String] -> (Path, FileMap) -> (Path, FileMap)
cmd ('c':'d':' ':dir) output (p, m) = (cd dir p, m)
  where cd :: String -> Path -> Path
        cd ".." (_:ds) = ds
        cd "/" _ = ["/"]
        cd d ds = d:ds
cmd ('l':'s':_) output (p, m) = (p, ls output p m)
  where ls :: [String] -> Path -> FileMap -> FileMap
        ls [] _ m = m
        ls (o:os) p m = ls os p $ case words o of
                                   ["dir", name] -> M.insert (reverse (name:p)) (Directory []) m
                                   [size, name]  -> M.insert (reverse (name:p)) (File (read size)) m

main = do
  inp <- map lines . tail .  splitOn "$ " <$> getContents
  let (_, filesystemMap) = foldl' (\acc (c:output) -> cmd c output acc)
                                  ([], M.fromList [(["/"], Directory [])])
                                  inp
  let sizeOf (File size) = size
      sizeOf (Directory fs) = sum $ map sizeOf fs
  let isDirectory (Directory _) = True
      isDirectory _ = False
  let directorySizes = map sizeOf $ filter isDirectory $ toList $ toTree filesystemMap ["/"]
  print (sum $ filter (<=100000) directorySizes)
  let needToDelete = 30000000 - (70000000 - maximum directorySizes)
  -- whatever man
  print (minimum $ map snd $ filter fst $ map (\d -> (d > needToDelete, d)) directorySizes)
