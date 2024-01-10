module Main where

import PEG
import System.Environment

-- a*b*
g1 :: PEG
g1 = PEG ['a', 'b']
         [("S", Seq (Star (Term 'a')) (Star (Term 'b')))]
         (Nonterm "S")

-- (ac)^n (c*d | cd*) (db)^n
g2 :: PEG
g2 = PEG ['a', 'b', 'c', 'd']
         [("S", Seq (Term 'a') (Seq (Nonterm "T") (Term 'b'))),
          ("T", Choice (Seq (Term 'c') (plus (Term 'd')))
                       (Choice (Seq (plus (Term 'c')) (Term 'd'))
                               (Seq (Term 'c') (Seq (Nonterm "S") (Term 'd')))))]
         (Nonterm "S")

-- Expr
g3 :: PEG
g3 = PEG ['0', '1', '+', '*', '^', '(', ')']
         [("S", Seq (Nonterm "M") (Star (Seq (Term '+') (Nonterm "M")))),
          ("M", Seq (Nonterm "E") (Star (Seq (Term '*') (Nonterm "E")))),
          ("E", Seq (Nonterm "V") (qmark (Seq (Term '^') (Nonterm "V")))),
          ("V", Choice (Term '0') (Choice (Term '1') (Seq (Term '(') (Seq (Nonterm "S") (Term ')')))))]
         (Nonterm "S")

-- a^n b^n c^n
g4 :: PEG
g4 = PEG ['a', 'b', 'c']
         [("S", Seq (amp (Seq (Nonterm "A") (Term 'c'))) (Seq (plus (Term 'a')) (Nonterm "B"))),
          ("A", Seq (Term 'a') (Seq (qmark (Nonterm "A")) (Term 'b'))),
          ("B", Seq (Term 'b') (Seq (qmark (Nonterm "B")) (Term 'c')))]
         (Nonterm "S")

-- Dyck-1
g5 :: PEG
g5 = PEG ['(', ')']
         [("S", Choice (Seq (Term '(') (Seq (Nonterm "S") (Seq (Term ')') (Nonterm "S")))) Eps)]
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