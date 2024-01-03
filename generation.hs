import System.Environment

data PEG = PEG [Char] [(String, Expr)] Expr

data Expr = Eps
          | Term Char
          | Nonterm String
          | Seq Expr Expr
          | Choice Expr Expr
          | Star Expr
          | Not Expr

qmark :: Expr -> Expr
qmark = flip Choice Eps

plus :: Expr -> Expr
plus e = Seq e (Star e)

amp :: Expr -> Expr
amp = Not . Not

interpret :: PEG -> Expr -> [Char] -> (Int, Maybe [Char])
interpret p Eps x = (1, Just [])
interpret p (Term c) x = case x of
                            [] -> (1, Nothing)
                            (a : as) -> if (a == c) then (1, Just [c]) else (1, Nothing)
interpret p@(PEG _ r _) (Nonterm n) x = case (lookup n r) of
                                         Just e -> interpret p e x
                                         Nothing -> (1, Nothing)
interpret p (Seq e1 e2) x = let (n1, x1) = interpret p e1 x
                            in case x1 of
                                Nothing -> (n1+1, Nothing)
                                Just y1 -> let (n2, x2) = interpret p e2 (drop (length y1) x)
                                           in case x2 of
                                               Nothing -> (n1+n2+1, Nothing)
                                               Just y2 -> (n1+n2+1, Just $ y1 ++ y2)
interpret p (Choice e1 e2) x = let (n1, x1) = interpret p e1 x
                               in case x1 of
                                    Nothing -> let (n2, x2) = interpret p e2 x
                                               in case x2 of
                                                    Nothing -> (n1+n2+1, Nothing)
                                                    Just y2 -> (n1+n2+1, Just y2)
                                    Just y1 -> (n1+1, Just y1)
interpret p (Star e1) x = let (n1, x1) = interpret p e1 x
                          in case x1 of
                                Nothing -> (n1+1, Just [])
                                Just y1 -> let (n2, x2) = interpret p (Star e1) (drop (length y1) x)
                                           in case x2 of
                                                Nothing -> (n1+n2+1, Just $ y1)
                                                Just y2 -> (n1+n2+1, Just $ y1 ++ y2)
interpret p (Not e1) x = let (n1, x1) = interpret p e1 x
                         in case x1 of
                              Nothing -> (n1+1, Just [])
                              Just _ -> (n1+1, Nothing)

g1 :: PEG
g1 = PEG ['a', 'b']
         [("S", Seq (Star (Term 'a')) (Star (Term 'b')))]
         (Nonterm "S")

g2 :: PEG
g2 = PEG ['a', 'b', 'c', 'd']
         [("S", Seq (Term 'a') (Seq (Nonterm "T") (Term 'b'))),
          ("T", Choice (Seq (Term 'c') (plus (Term 'd')))
                       (Choice (Seq (plus (Term 'c')) (Term 'd'))
                               (Seq (Term 'c') (Seq (Nonterm "S") (Term 'd')))))]
         (Nonterm "S")

g3 :: PEG
g3 = PEG ['0', '1', '+', '*', '^', '(', ')']
         [("S", Seq (Nonterm "M") (Star (Seq (Term '+') (Nonterm "M")))),
          ("M", Seq (Nonterm "E") (Star (Seq (Term '*') (Nonterm "E")))),
          ("E", Seq (Nonterm "V") (qmark (Seq (Term '^') (Nonterm "V")))),
          ("V", Choice (Term '0') (Choice (Term '1') (Seq (Term '(') (Seq (Nonterm "S") (Term ')')))))]
         (Nonterm "S")

g4 :: PEG
g4 = PEG ['a', 'b', 'c']
         [("S", Seq (amp (Seq (Nonterm "A") (Term 'c'))) (Seq (plus (Term 'a')) (Nonterm "B"))),
          ("A", Seq (Term 'a') (Seq (qmark (Nonterm "A")) (Term 'b'))),
          ("B", Seq (Term 'b') (Seq (qmark (Nonterm "B")) (Term 'c')))]
         (Nonterm "S")

g5 :: PEG
g5 = PEG ['a', 'b', 'c']
         [("S",  Seq (Nonterm "AB") (Star (Term 'c'))),
          ("AB", Choice (Seq (Term 'a') (Seq (Nonterm "AB") (Term 'b'))) (amp (Nonterm "BC"))),
          ("BC", qmark (Seq (Term 'b') (Seq (Nonterm "BC") (Term 'c'))))]
         (Nonterm "S")

main :: IO ()
main = do args <- getArgs
          let [inp, gS] = args
          let g = case gS of
                    "g1" -> g1; "g2" -> g2; "g3" -> g3; "g4" -> g4; "g5" -> g5
     -- Pass len; iterate here
          let n :: Int = read inp
          let PEG alph _ _ = g
          let ap = (\s -> map (flip ($) s) (map (:) alph))
          mapM_ (\s -> do let (_, res) = interpret g (Nonterm "S") s
                          case res of 
                              Nothing -> return ()
                              Just x -> if (length x == n) then putStrLn x else return ())
                (foldl (>>=) [""] (replicate n ap))
          return ()
     -- Pass string; iterate outside
          --let (n, r) = interpret g (Nonterm "S") inp
          --case r of
          --     Nothing -> return ()
          --     Just x -> if (length x == length inp) then putStrLn inp else return ()