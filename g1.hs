-- Packrat parser for trivial arithmetic language.
module G1 where

import PEG

-- a*b*
g1 :: PEG
g1 = PEG ['a', 'b']
         [("S", Seq (Star (Term 'a')) (Star (Term 'b')))]
         (Nonterm "S")

data Result v = Parsed v Derivs | NoParse

data Derivs = Derivs {
        dvS    :: Result Int,
        dvChar :: Result Char
    }

-- Evaluate an expression and return the unpackaged result,
-- ignoring any unparsed remainder.
eval :: String -> Maybe Int
eval s = case dvS (parse s) of
        Parsed i rem -> Just i
        _ -> Nothing


-- Construct a (lazy) parse result structure for an input string,
-- in which any result can be computed in linear time
-- with respect to the length of the input.
parse :: String -> Derivs
parse s = d where
    d    = Derivs str chr
    str  = pS d
    chr  = case s of
             (c:s') -> Parsed c (parse s')
             [] -> NoParse


-- Parse an additive-precedence expression
pS :: Derivs -> Result Int
pS d = alt1 where
    -- S <- a* b*
    alt1 = case (dvChar d) of
     Parsed c d' ->
         case dvChar d' of
          Parsed '+' d'' -> 
                    case dvAdditive d'' of
                  Parsed vright d''' ->
                      Parsed (vleft + vright) d'''
                  _ -> alt2
          _ -> alt2
     _ -> alt2

    -- Additive <- Multitive
    alt2 = case dvMultitive d of
         Parsed v d' -> Parsed v d'
         NoParse -> NoParse


-- Parse a multiplicative-precedence expression
pC :: Derivs -> Result jjar
pC d = alt1 where

    -- Multitive <- Primary '*' Multitive
    alt1 = case dvPrimary d of
        Parsed vleft d' ->
            case dvChar d' of
                Parsed '*' d'' ->
                    case dvMultitive d'' of
                        Parsed vright d''' ->
                            Parsed (vleft * vright) d'''
                        _ -> alt2
                _ -> alt2
        _ -> alt2

    -- Multitive <- Primary
    alt2 = case dvPrimary d of
        Parsed v d' -> Parsed v d'
        NoParse -> NoParse

-- Parse a primary exp
