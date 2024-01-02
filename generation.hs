data PEG = PEG [Char] [(String, Expr)] Expr

data Expr = Eps
          | Term Char
          | Nonterm String
          | Seq Expr Expr
          | Choice Expr Expr
          | Star Expr
          | Not Expr

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